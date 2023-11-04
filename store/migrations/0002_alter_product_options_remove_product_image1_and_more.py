# Generated by Django 4.2.5 on 2023-10-17 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'product', 'verbose_name_plural': 'products'},
        ),
        migrations.RemoveField(
            model_name='product',
            name='image1',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image2',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image3',
        ),
        migrations.RemoveField(
            model_name='product',
            name='images',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=20)),
                ('stock', models.PositiveIntegerField(default=None)),
                ('selling_price', models.DecimalField(decimal_places=2, default=None, max_digits=10)),
                ('actual_price', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10)),
                ('is_available', models.BooleanField(default=True)),
                ('image1', models.ImageField(default=None, upload_to='photos/products/')),
                ('image2', models.ImageField(default=None, upload_to='photos/products/')),
                ('image3', models.ImageField(default=None, upload_to='photos/products/')),
                ('image4', models.ImageField(default=None, upload_to='photos/products/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='store.product')),
            ],
            options={
                'verbose_name': 'variation',
                'verbose_name_plural': 'variations',
            },
        ),
        migrations.CreateModel(
            name='VariantImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default=None, upload_to='photos/products/')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.variation')),
            ],
        ),
    ]