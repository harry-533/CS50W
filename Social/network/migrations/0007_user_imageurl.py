# Generated by Django 5.0.6 on 2024-05-30 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_post_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='imageURL',
            field=models.URLField(blank=True, max_length=256, null=True),
        ),
    ]
