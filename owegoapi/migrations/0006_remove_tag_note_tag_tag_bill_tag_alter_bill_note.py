# Generated by Django 4.0.3 on 2022-03-15 02:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('owegoapi', '0005_bill_owegouser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='note_tag',
        ),
        migrations.AddField(
            model_name='tag',
            name='bill_tag',
            field=models.ManyToManyField(to='owegoapi.bill'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='note',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='owegoapi.note'),
        ),
    ]
