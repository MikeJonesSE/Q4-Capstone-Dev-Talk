# Generated by Django 3.2.5 on 2021-07-18 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_users', '0003_alter_uzer_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uzer',
            name='avatar',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]