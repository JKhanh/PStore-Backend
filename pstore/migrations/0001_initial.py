# Generated by Django 3.2.8 on 2021-10-27 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=200)),
                ('lastname', models.CharField(max_length=100)),
                ('birthday', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('type', models.CharField(choices=[('PH', 'Phone'), ('AC', 'Accessory'), ('EL', 'Electronic')], default='PH', max_length=2)),
                ('basePrice', models.FloatField(default=0)),
                ('sale', models.FloatField(default=0)),
                ('image', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField()),
                ('comment', models.CharField(max_length=500)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pstore.product')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pstore.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pstore.customer')),
            ],
        ),
        migrations.CreateModel(
            name='ItemCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pstore.customer')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pstore.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pstore.product')),
            ],
        ),
    ]
