import os
import pandas as pd
import gzip
import redis
from datetime import datetime as dt
from .models import DSP, DSR
from .serializers import DSRSerializer, DSPSerializer
from digital import settings
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics, permissions
from .serializers import UserSerializer, CreateUserSerializer, LoginUserSerializer, \
    LogoutUserSerializer, ChangePasswordSerializer
from rest_framework.views import APIView
from rest_framework import parsers, renderers, status
from rest_framework.response import Response


class DSRViewSet(viewsets.ModelViewSet):
    queryset = DSR.objects.all()
    serializer_class = DSRSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class DSPViewSet(viewsets.ModelViewSet):
    queryset = DSP.objects.all()
    serializer_class = DSPSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        territory = self.request.GET.get('territory')
        period_start = self.request.GET.get('period_start')
        period_end = self.request.GET.get('period_end')
        query = DSR.objects.all().filter(period_start = period_start, period_end = period_end).first()
        resp = self.queryset.filter(dsrs = query).first()
        return [resp]

    def post(self, request, *args, **kwargs):
        r = redis.StrictRedis(host=settings.REDIS_HOST,
                              port=settings.REDIS_PORT, db=0)
        obj = DSR.objects.all()
        pwd = os.getcwd()
        with os.scandir('{path}/data'.format(path=pwd)) as entries:
            for entry in entries:
                """
                Check file in Redis, if exist, don't insert records to database.
                """
                if not r.get(entry.name):
                    for model in obj:
                        with gzip.open('{path}/data/{file}'.format(path=pwd,file=entry.name),'rb') as z:
                                dataset = pd.read_csv(z, header=0, delimiter="\t")
                                dataset['dsrs'] = model
                                DSP.objects.bulk_create(
                                    DSP(**vals) for vals in dataset.to_dict('records')
                                )
                    r.mset({"{file}".format(file=entry.name) : "{date}".format(date=dt.now())})
            return Response({"msg": "Files has been written in db succesfully."})


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class LoginAPI(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LoginUserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": str(Token.objects.get_or_create(user=user)[0])
        })

class LogoutAPI(APIView):
    queryset = User.objects.all()
    serializer_class = LogoutUserSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class RegistrationAPI(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": str(Token.objects.create(user=user))
        })

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })




