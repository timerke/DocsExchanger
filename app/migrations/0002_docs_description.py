# Generated by Django 3.1.2 on 2020-11-05 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='docs',
            name='description',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
