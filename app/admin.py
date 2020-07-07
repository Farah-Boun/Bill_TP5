from django.contrib import admin

from django.contrib import admin
from app.models import Client, Produit, Facture, LigneFacture

# Register your models here.
admin.site.register(Client)
admin.site.register(Facture)
admin.site.register(Produit)
admin.site.register(LigneFacture)
