# Generated by Django 5.0.2 on 2024-02-29 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0005_rename_topic_module_course"),
    ]

    operations = [
        migrations.AlterField(
            model_name="module",
            name="text",
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
