# Generated by Django 5.0.2 on 2024-04-04 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0021_alter_quiz_module"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Answer",
            new_name="Choice",
        ),
    ]