# Generated by Django 5.0.4 on 2024-04-22 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_alter_products_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='capacity',
        ),
        migrations.RemoveField(
            model_name='products',
            name='color',
        ),
        migrations.RemoveField(
            model_name='products',
            name='country',
        ),
        migrations.RemoveField(
            model_name='products',
            name='document',
        ),
        migrations.RemoveField(
            model_name='products',
            name='memory',
        ),
        migrations.RemoveField(
            model_name='products',
            name='status',
        ),
        migrations.AddField(
            model_name='products',
            name='capacity',
            field=models.ManyToManyField(related_name='products', to='db.capacities', verbose_name='Yomkosti'),
        ),
        migrations.AddField(
            model_name='products',
            name='color',
            field=models.ManyToManyField(related_name='products', to='db.colors', verbose_name='Rangi'),
        ),
        migrations.AddField(
            model_name='products',
            name='country',
            field=models.ManyToManyField(related_name='products', to='db.countries', verbose_name='Mamlakat'),
        ),
        migrations.AddField(
            model_name='products',
            name='document',
            field=models.ManyToManyField(related_name='products', to='db.documents', verbose_name='Hujjat'),
        ),
        migrations.AddField(
            model_name='products',
            name='memory',
            field=models.ManyToManyField(related_name='products', to='db.memories', verbose_name='Xotira'),
        ),
        migrations.AddField(
            model_name='products',
            name='status',
            field=models.ManyToManyField(related_name='products', to='db.statuses', verbose_name='Holati'),
        ),
    ]
