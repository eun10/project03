# Generated by Django 3.2 on 2022-11-09 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0003_alter_post_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='expiration_date',
            field=models.DateField(),
        ),
    ]
