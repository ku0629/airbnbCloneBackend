# Generated by Django 4.2.3 on 2023-08-01 11:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("categories", "0002_alter_category_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name_plural": "Categories"},
        ),
    ]
