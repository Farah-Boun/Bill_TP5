from django.db import models
from django import utils
import datetime

# Create your models here.
from django.views.generic import DetailView
from django_tables2 import tables


class Client(models.Model):
    SEXE = (
        ('M', 'Masculin'),
        ('F', 'Feminin')
    )
    nom = models.CharField(max_length=50, null=True, blank=True)
    prenom = models.CharField(max_length=50, null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    tel = models.CharField(max_length = 10, null=True, blank=True)
    sexe = models.CharField(max_length=1, choices = SEXE)
    
    def __str__(self):
        return self.nom + ' ' + self.prenom


class Fournisseur(models.Model):
    designation = models.CharField(max_length=50)

class Produit(models.Model):
    designation = models.CharField(max_length=50)
    prix = models.FloatField(default=0)
    fournisseur =  models.ForeignKey(Fournisseur, on_delete=models.CASCADE, related_name='produits', default=1)
    def __str__(self):
        return self.designation
    
    
class Facture(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField(default=utils.timezone.now)

    @property
    def calcul_facture_totale(self):
        total = 0
        for ligne in LigneFacture.objects.all(): 
            if (ligne.facture==self):
                total += (ligne.produit.prix * ligne.qte)
            
        return total



class LigneFacture(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    qte = models.IntegerField(default=1)
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='lignes')
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['produit', 'facture'], name="produit-facture")
        ]

