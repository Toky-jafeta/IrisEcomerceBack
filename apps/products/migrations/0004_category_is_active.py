# Generated by Django 4.2.9 on 2024-02-05 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
