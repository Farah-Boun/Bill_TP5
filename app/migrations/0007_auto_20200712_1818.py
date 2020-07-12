# Generated by Django 3.0.8 on 2020-07-12 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20200708_0348'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='photo',
            field=models.ImageField(default='banniere.png', upload_to='media'),
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Client')),
                ('produits', models.ManyToManyField(to='app.Produit')),
            ],
        ),
    ]
