# Generated by Django 3.2.8 on 2022-03-30 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_auto_20220330_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='source',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
