# Generated by Django 4.0.5 on 2022-06-16 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MainProg', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='title',
        ),
    ]
