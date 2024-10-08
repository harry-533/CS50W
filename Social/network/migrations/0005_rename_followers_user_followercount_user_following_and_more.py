# Generated by Django 5.0.6 on 2024-05-29 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_remove_user_following_userfollowing'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='followers',
            new_name='followerCount',
        ),
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.JSONField(default=list),
        ),
        migrations.DeleteModel(
            name='UserFollowing',
        ),
    ]
