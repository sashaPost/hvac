# Generated by Django 5.0.3 on 2024-04-02 13:34

import ckeditor_uploader.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField()),
                ('preview_image', models.ImageField(upload_to='images')),
                ('preview_image_alt', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='VehicleType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('FE', 'Fuel Engine'), ('EV', 'Electric Vehicle')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CaseImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images')),
                ('image_alt', models.CharField(blank=True, max_length=255)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.case')),
            ],
        ),
        migrations.CreateModel(
            name='FuelEngineVehicle',
            fields=[
                ('vehicle_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cases.vehicle')),
                ('engine_capacity', models.DecimalField(decimal_places=1, max_digits=3)),
            ],
            bases=('cases.vehicle',),
        ),
        migrations.AddField(
            model_name='case',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.vehicle'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='vehicle_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.vehicletype'),
        ),
    ]
