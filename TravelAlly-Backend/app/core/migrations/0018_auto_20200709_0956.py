# Generated by Django 3.0.4 on 2020-07-09 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20200709_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='user_name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]