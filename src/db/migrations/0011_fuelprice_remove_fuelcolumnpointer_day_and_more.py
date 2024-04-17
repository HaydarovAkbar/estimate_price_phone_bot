# Generated by Django 4.2.10 on 2024-03-31 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0010_rename_plastig_size_salefuel_card_size_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FuelPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(verbose_name='Narxi')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan sana')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name="O'zgartirilgan sana")),
                ('fuel_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.fueltype', verbose_name="Yoqilg'i turi")),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.organization', verbose_name='Tashkilot')),
            ],
            options={
                'verbose_name': "Yoqilg'i narxi",
                'verbose_name_plural': "Yoqilg'i narxlari",
                'db_table': 'fuel_price',
            },
        ),
        migrations.RemoveField(
            model_name='fuelcolumnpointer',
            name='day',
        ),
        migrations.AddField(
            model_name='salefuel',
            name='benefit',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Fuel',
        ),
        migrations.AddIndex(
            model_name='fuelprice',
            index=models.Index(fields=['fuel_type'], name='fuel_price_fuel_ty_cd8d92_idx'),
        ),
    ]