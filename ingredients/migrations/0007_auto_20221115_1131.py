# Generated by Django 3.2 on 2022-11-15 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0006_auto_20221114_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipelist',
            name='rc_rec',
            field=models.IntegerField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='recipelist',
            name='rc_scrap',
            field=models.IntegerField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='recipelist',
            name='rc_view',
            field=models.IntegerField(blank=True, max_length=100, null=True),
        ),
    ]
