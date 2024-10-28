# Generated by Django 5.0.3 on 2024-10-28 19:35

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cases", "0006_alter_aboutimage_image_alt_alter_aboutmessage_title_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="servicecategory",
            options={
                "ordering": ["name"],
                "verbose_name": "Service Category",
                "verbose_name_plural": "Service Categories",
            },
        ),
        migrations.RemoveField(
            model_name="case",
            name="timestamp",
        ),
        migrations.AddField(
            model_name="aboutmessage",
            name="created_at",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Created At"
            ),
        ),
        migrations.AddField(
            model_name="aboutmessage",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated At"),
        ),
        migrations.AddField(
            model_name="case",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated At"),
        ),
        migrations.AddField(
            model_name="caseimage",
            name="created_at",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Created At"
            ),
        ),
        migrations.AddField(
            model_name="caseimage",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated At"),
        ),
        migrations.AddField(
            model_name="contact",
            name="created_at",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Created At"
            ),
        ),
        migrations.AddField(
            model_name="contact",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated At"),
        ),
        migrations.AddField(
            model_name="servicecategory",
            name="created_at",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Created At"
            ),
        ),
        migrations.AddField(
            model_name="servicecategory",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated At"),
        ),
        migrations.AlterField(
            model_name="aboutimage",
            name="about_image",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="cases.aboutmessage",
                verbose_name="About Message",
            ),
        ),
        migrations.AlterField(
            model_name="aboutimage",
            name="image",
            field=models.ImageField(upload_to="images", verbose_name="Image"),
        ),
        migrations.AlterField(
            model_name="aboutimage",
            name="image_alt",
            field=models.CharField(
                blank=True, max_length=255, verbose_name="Image Alt"
            ),
        ),
        migrations.AlterField(
            model_name="case",
            name="added_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Added By",
            ),
        ),
        migrations.AlterField(
            model_name="case",
            name="created_at",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Created At"
            ),
        ),
        migrations.AlterField(
            model_name="case",
            name="main_page_visibility",
            field=models.BooleanField(
                default=True, verbose_name="Main Page Visibility"
            ),
        ),
        migrations.AlterField(
            model_name="case",
            name="preview_image",
            field=models.ImageField(upload_to="images", verbose_name="Preview Image"),
        ),
        migrations.AlterField(
            model_name="case",
            name="preview_image_alt",
            field=models.CharField(
                blank=True, max_length=255, verbose_name="Preview Image Alt"
            ),
        ),
        migrations.AlterField(
            model_name="caseimage",
            name="case",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="case",
                to="cases.case",
            ),
        ),
        migrations.AlterField(
            model_name="caseimage",
            name="image",
            field=models.ImageField(upload_to="images", verbose_name="Image"),
        ),
        migrations.AlterField(
            model_name="caseimage",
            name="image_alt",
            field=models.CharField(
                blank=True, max_length=255, verbose_name="Image Alt"
            ),
        ),
        migrations.AlterField(
            model_name="contact",
            name="email",
            field=models.EmailField(max_length=254, verbose_name="Email"),
        ),
        migrations.AlterField(
            model_name="contact",
            name="instagram_link",
            field=models.URLField(blank=True, verbose_name="Instagram"),
        ),
        migrations.AlterField(
            model_name="contact",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                max_length=128, region=None, verbose_name="Phone Number"
            ),
        ),
        migrations.AlterField(
            model_name="contact",
            name="telegram_link",
            field=models.URLField(blank=True, verbose_name="Telegram"),
        ),
        migrations.AlterField(
            model_name="service",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="services",
                to="cases.servicecategory",
                verbose_name="Category",
            ),
        ),
        migrations.AlterField(
            model_name="service",
            name="created_at",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Created At"
            ),
        ),
        migrations.AlterField(
            model_name="service",
            name="icon",
            field=models.ImageField(
                blank=True, upload_to="images", verbose_name="Icon"
            ),
        ),
        migrations.AlterField(
            model_name="service",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Is Active"),
        ),
        migrations.AlterField(
            model_name="service",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated At"),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="case",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="vehicle",
                to="cases.case",
                verbose_name="Case",
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="engine_capacity",
            field=models.DecimalField(
                blank=True,
                decimal_places=1,
                help_text="In litres",
                max_digits=3,
                null=True,
                verbose_name="Engine Capacity",
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="vehicle_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="vehicles",
                to="cases.vehicletype",
                verbose_name="Vehicle Type",
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="year",
            field=models.PositiveIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(1900),
                    django.core.validators.MaxValueValidator(2025),
                ],
                verbose_name="Year",
            ),
        ),
        migrations.AlterField(
            model_name="vehicletype",
            name="name",
            field=models.CharField(
                choices=[
                    ("FE", "Fuel Engine"),
                    ("EV", "Electric Vehicle"),
                    ("HY", "Hybrid Vehicle"),
                ],
                db_index=True,
                max_length=100,
                verbose_name="Type",
            ),
        ),
        migrations.AddIndex(
            model_name="case",
            index=models.Index(
                fields=["main_page_visibility"], name="cases_case_main_pa_15b7af_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="service",
            index=models.Index(
                fields=["is_active"], name="cases_servi_is_acti_af7e37_idx"
            ),
        ),
    ]
