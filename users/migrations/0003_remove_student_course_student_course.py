# Generated by Django 5.0.2 on 2024-03-04 06:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0009_uploadvideo_slug"),
        ("users", "0002_student"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="student",
            name="Course",
        ),
        migrations.AddField(
            model_name="student",
            name="course",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="courses.course",
            ),
        ),
    ]