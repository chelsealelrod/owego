# Generated by Django 4.0.3 on 2022-03-12 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('owegoapi', '0004_owegouser'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='owegouser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='owegoapi.owegouser'),
        ),
    ]
