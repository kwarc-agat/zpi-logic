# Generated by Django 3.1.5 on 2021-01-13 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zpiapi', '0002_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='type',
            field=models.CharField(choices=[('0', 'Normal'), ('1', 'Invitation')], default='0', max_length=20),
        ),
    ]
