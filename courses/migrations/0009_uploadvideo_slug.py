# Generated by Django 5.0.2 on 2024-02-29 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0008_rename_title_course_title_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="uploadvideo",
            name="slug",
            field=models.SlugField(blank=True, unique=True),
        ),
    ]