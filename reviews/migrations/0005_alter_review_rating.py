# Generated by Django 4.2.3 on 2023-09-01 13:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reviews", "0004_alter_review_rating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="rating",
            field=models.PositiveIntegerField(),
        ),
    ]
