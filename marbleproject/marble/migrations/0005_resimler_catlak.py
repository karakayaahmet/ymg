# Generated by Django 4.1 on 2023-01-04 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("marble", "0004_alter_resimler_options_resimler_created_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="resimler",
            name="catlak",
            field=models.ImageField(default=1, upload_to="catlak/"),
            preserve_default=False,
        ),
    ]
