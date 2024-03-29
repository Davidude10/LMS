# Generated by Django 5.0.2 on 2024-03-20 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0015_alter_module_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="image",
            field=models.ImageField(
                default="default.png", null=True, upload_to="course_icon/%Y/%m/%d/"
            ),
        ),
    ]
