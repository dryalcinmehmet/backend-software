# Generated by Django 3.1 on 2021-07-18 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dsrs', '0006_auto_20210718_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dsr',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dsrs', to='dsrs.currency'),
        ),
        migrations.AlterField(
            model_name='dsr',
            name='territory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dsrs', to='dsrs.territory'),
        ),
    ]
