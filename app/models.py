from django.db import models
from django import utils
import datetime

# Create your models here.
from django.db.models import *
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

    @property
    def calcul(self):
        return "Testo"


class Fournisseur(models.Model):
    designation = models.CharField(max_length=50)
    adresse = models.CharField(max_length=50)

    def __str__(self):
        return self.designation


class Produit(models.Model):
    photo = models.ImageField(upload_to='media', default='banniere.png')
    designation = models.CharField(max_length=50)
    prix = models.FloatField(default=0)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, related_name='produits', default=1)

    def __str__(self):
        return self.designation

    def serialize(self):
        return self.__dict__
    
    
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
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='factures')
    qte = models.IntegerField(default=1)
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='lignes')
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['produit', 'facture'], name="produit-facture")
        ]


class Commande(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    produits = models.ManyToManyField(Produit)


class PanierItem(models.ManyToManyField):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    qte = models.IntegerField(default=1)

    def serialize(self):
        return self.__dict__

class PanierLine(object):
    def __init__(self, id, qte):
        self.id = id
        self.qte = qte

    def serialize(self):
        return self.__dict__
