# Generated by Django 3.1.2 on 2020-11-05 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_docs_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='token',
            field=models.UUIDField(null=True),
        ),
    ]
