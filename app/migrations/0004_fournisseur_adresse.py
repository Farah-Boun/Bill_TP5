# Generated by Django 3.0.8 on 2020-07-07 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_produit_fournisseur'),
    ]

    operations = [
        migrations.AddField(
            model_name='fournisseur',
            name='adresse',
            field=models.CharField(default='Alger', max_length=50),
        ),
    ]
