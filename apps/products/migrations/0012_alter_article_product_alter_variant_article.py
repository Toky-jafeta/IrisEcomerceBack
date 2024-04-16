# Generated by Django 4.2.9 on 2024-02-06 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='products.product'),
        ),
        migrations.AlterField(
            model_name='variant',
            name='article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='products.article'),
        ),
    ]
