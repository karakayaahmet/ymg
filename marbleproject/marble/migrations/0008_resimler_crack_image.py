# Generated by Django 4.1 on 2023-01-18 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("marble", "0007_alter_resimler_average_color"),
    ]

    operations = [
        migrations.AddField(
            model_name="resimler",
            name="crack_image",
            field=models.ImageField(blank=True, upload_to="catlak/"),
        ),
    ]
