# Generated by Django 5.0.2 on 2024-03-12 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0003_alter_quiz_options_quiz_draft_quiz_pass_mark_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sitting",
            name="course",
        ),
        migrations.RemoveField(
            model_name="sitting",
            name="quiz",
        ),
        migrations.RemoveField(
            model_name="sitting",
            name="user",
        ),
        migrations.RemoveField(
            model_name="question",
            name="quiz",
        ),
        migrations.AlterField(
            model_name="quiz",
            name="category",
            field=models.TextField(
                blank=True,
                choices=[("assignment", "Assignment"), ("practice", "Practice Quiz")],
            ),
        ),
        migrations.DeleteModel(
            name="EssayQuestion",
        ),
        migrations.DeleteModel(
            name="Sitting",
        ),
    ]