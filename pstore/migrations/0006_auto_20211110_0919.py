# Generated by Django 3.2.8 on 2021-11-10 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pstore', '0005_alter_cart_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemcart',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='pstore.cart'),
        ),
        migrations.AlterField(
            model_name='itemorder',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='pstore.order'),
        ),
    ]
