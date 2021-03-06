# Generated by Django 3.1.8 on 2021-07-17 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dsrs', '0001_initial'),
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
        migrations.AlterField(
            model_name='territory',
            name='local_currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='territories', to='dsrs.currency'),
        ),
        migrations.CreateModel(
            name='DSP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dsp_id', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('artists', models.CharField(max_length=255)),
                ('isrc', models.CharField(max_length=255)),
                ('revenue', models.FloatField()),
                ('dsrs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dsp', to='dsrs.dsr')),
            ],
            options={
                'db_table': 'dsp',
            },
        ),
    ]
