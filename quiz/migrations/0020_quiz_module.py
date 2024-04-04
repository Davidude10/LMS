# Generated by Django 5.0.2 on 2024-04-04 14:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0018_delete_activitylog_chapter_slug_chapter_summary_and_more"),
        ("quiz", "0019_remove_quiz_desc_quiz_course"),
    ]

    operations = [
        migrations.AddField(
            model_name="quiz",
            name="Module",
            field=models.ForeignKey(
                limit_choices_to={
                    "course": models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="courses.course",
                    )
                },
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="courses.module",
            ),
        ),
    ]
