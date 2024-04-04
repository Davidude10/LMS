# Generated by Django 5.0.2 on 2024-04-04 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0017_remove_quizattempt_quiz_remove_quizattempt_user_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="answer",
            name="content",
        ),
        migrations.RemoveField(
            model_name="question",
            name="content",
        ),
        migrations.RemoveField(
            model_name="quiz",
            name="name",
        ),
        migrations.AddField(
            model_name="answer",
            name="Choice",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="question",
            name="Question",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="quiz",
            name="Quiz_name",
            field=models.CharField(max_length=50, null=True),
        ),
    ]