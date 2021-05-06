# Generated by Django 3.0.4 on 2020-07-09 09:31

from django.db import migrations
import uuid


def gen_uuid(apps, schema_editor):
    MyModel = apps.get_model('core', 'UserModel')
    for row in MyModel.objects.all():
        row.user_name = uuid.uuid4()
        print(row.user_name)
        row.save(update_fields=['user_name'])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_usermodel_user_name'),
    ]

    operations = [
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
    ]