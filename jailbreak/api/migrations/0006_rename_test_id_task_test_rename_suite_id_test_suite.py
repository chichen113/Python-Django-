# Generated by Django 4.1 on 2024-07-25 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_remove_suite_test_id_remove_test_task_id_and_more"),
    ]

    operations = [
        migrations.RenameField(model_name="task", old_name="test_id", new_name="test",),
        migrations.RenameField(
            model_name="test", old_name="suite_id", new_name="suite",
        ),
    ]
