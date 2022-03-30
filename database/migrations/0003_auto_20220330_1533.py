# Generated by Django 3.2.8 on 2022-03-30 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_auto_20220325_1225'),
    ]

    operations = [
        migrations.CreateModel(
            name='object',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('text', models.CharField(max_length=100)),
            ],
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='receipt_id',
            new_name='receipt',
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='sender_id',
            new_name='sender',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='activity_type',
        ),
        migrations.DeleteModel(
            name='activity_type',
        ),
        migrations.AlterField(
            model_name='notification',
            name='object_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.object'),
        ),
        migrations.DeleteModel(
            name='object_type',
        ),
    ]
