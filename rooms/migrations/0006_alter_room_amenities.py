# Generated by Django 4.2.3 on 2023-11-01 11:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rooms", "0005_alter_room_amenities_alter_room_category_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="room",
            name="amenities",
            field=models.ManyToManyField(
                blank=True, related_name="rooms", to="rooms.amenity"
            ),
        ),
    ]