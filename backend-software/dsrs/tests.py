from . import models
from . import serializers
from django.test import TestCase
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.test import client
from django.shortcuts import reverse

class GetSingleDSRTest(TestCase):
    """ Test module for GET single dsr API """

    def setUp(self):

        self.dsr_obj = models.DSR.objects.create(
            path='/data/test.csv', period_start='2021-07-17', period_end='2021-07-19'
            )


    def test_get_valid_single_dsrs(self):
        response = client.get(
            reverse('get_delete_update_dsrs', kwargs={'pk': self.dsr_obj.pk}))
        dsrs = models.DSR.objects.get(pk=self.dsr_obj.pk)
        serializer = serializers.DSRSerializer(dsrs)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_dsrs(self):
        response = client.get(
            reverse('get_delete_update_dsrs', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @api_view(['GET', 'UPDATE', 'DELETE'])
    def get_delete_update_dsrs(request, pk):
        try:
            dsrs = models.DSR.objects.get(pk=pk)
        except models.DSR.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # get details of a single dsr
        if request.method == 'GET':
            serializer = serializers.DSRSerializer(dsrs)
            return Response(serializer.data)