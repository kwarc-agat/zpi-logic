# Generated by Django 3.1.5 on 2021-01-14 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zpiapi', '0003_auto_20210113_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='teamId',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='zpiapi.team'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='title',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='team',
            name='adminEmail',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='team',
            name='lecturer',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='zpiapi.teacher'),
        ),
        migrations.AlterField(
            model_name='team',
            name='subject',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='team',
            name='topic',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
