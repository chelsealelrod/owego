# Generated by Django 4.0.3 on 2022-03-20 22:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('owegoapi', '0010_rename_bill_billtag_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='bill',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='owegoapi.bill'),
        ),
    ]