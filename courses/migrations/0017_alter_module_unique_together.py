# Generated by Django 5.0.2 on 2024-03-21 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0016_course_image"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="module",
            unique_together={("course", "title")},
        ),
    ]