from bootstrap_datepicker_plus import DatePickerInput
from django.db.models import Sum, ExpressionWrapper, F, FloatField
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
import django_tables2 as tables
from django_tables2.config import RequestConfig
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML, Button
from django.urls import reverse
from django_tables2 import MultiTableMixin
from django.views.generic.base import TemplateView
from django.db.models import Count
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from app.models import Facture, LigneFacture, Client, Fournisseur, Produit, PanierItem, PanierLine


# Create your views here.

@login_required
def facture_detail_view(request, pk):
    facture = get_object_or_404(Facture, id=pk)
    context = {}
    context['facture'] = facture
    return render(request, 'bill/facture_detail.html', context)


class FactureUpdate(LoginRequiredMixin, UpdateView):
    login_url = '../../../accounts/login/'
    redirect_field_name = 'redirect_to'
    
    model = Facture
    fields = ['client', 'date']
    template_name = 'bill/update.html'


class LigneFactureTable(tables.Table):
    action = '<a href="{% url "lignefacture_update" pk=record.id facture_pk=record.facture.id %}" class="btn btn-warning">Modifier</a>\
            <a href="{% url "lignefacture_delete" pk=record.id facture_pk=record.facture.id %}" class="btn btn-danger">Supprimer</a>'
    edit = tables.TemplateColumn(action)

    class Meta:
        model = LigneFacture
        template_name = "django_tables2/bootstrap4.html"
        fields = ('produit__designation', 'produit__id', 'produit__prix', 'qte')


class FactureDetailView(DetailView):
    template_name = 'bill/facture_table_detail.html'
    model = Facture

    def get_context_data(self, **kwargs):
        context = super(FactureDetailView, self).get_context_data(**kwargs)

        table = LigneFactureTable(LigneFacture.objects.filter(facture=self.kwargs.get('pk')))
        RequestConfig(self.request, paginate={"per_page": 2}).configure(table)
        context['table'] = table
        return context


class LigneFactureCreateView(CreateView):
    model = LigneFacture
    template_name = 'bill/create.html'
    fields = ['facture', 'produit', 'qte']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['facture'] = forms.ModelChoiceField(
            queryset=Facture.objects.filter(id=self.kwargs.get('facture_pk')), initial=0)
        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('facture_table_detail', kwargs={'pk': self.kwargs.get('facture_pk')})
        return form


class LigneFactureUpdateView(UpdateView):
    model = LigneFacture
    template_name = 'bill/update.html'
    fields = ['facture', 'produit', 'qte']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['facture'] = forms.ModelChoiceField(
            queryset=Facture.objects.filter(id=self.kwargs.get('facture_pk')), initial=0)
        form.helper.add_input(Submit('submit', 'Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('facture_table_detail', kwargs={'pk': self.kwargs.get('facture_pk')})
        return form


class LigneFactureDeleteView(DeleteView):
    model = LigneFacture
    template_name = 'bill/delete.html'

    def get_success_url(self):
        self.success_url = reverse('facture_table_detail', kwargs={'pk': self.kwargs.get('facture_pk')})


class ClientTable(tables.Table):
    action = '<a href="{% url "client_update" pk=record.id  %}" class="btn btn-warning">Modifier</a>\
              <a href="{% url "client_delete" pk=record.id  %}" class="btn btn-danger">Supprimer</a>\
             <a href="{% url "client_factures_list" pk=record.id %}" class="btn btn-danger">Liste Factures</a>'
    edit = tables.TemplateColumn(action)

    class Meta:
        model = Client
        template_name = "django_tables2/bootstrap4.html"
        fields = ('id','nom', 'prenom', 'adresse', 'chiffre_affaire')





class ClientsView(ListView):
    model = Client
    template_name = 'bill/client_table.html'

    def get_context_data(self, **kwargs):
        context = super(ClientsView, self).get_context_data(**kwargs)

        queryset = Client.objects.values('id','nom', 'prenom', 'adresse').annotate(chiffre_affaire=Sum(
            ExpressionWrapper(F('facture__lignes__qte'), output_field=FloatField()) * F(
                'facture__lignes__produit__prix')))
        table = ClientTable(queryset)
        RequestConfig(self.request, paginate={"per_page": 10}).configure(table)
        context['table'] = table
        return context


class ClientCreateView(CreateView):
    model = Client
    template_name = 'bill/create_client.html'
    fields = ['id','nom', 'prenom', 'sexe', 'adresse', 'tel']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('client_table')
        return form


class ClientUpdateView(UpdateView):
    model = Client
    fields = ['nom', 'prenom', 'sexe', 'adresse', 'tel']
    template_name = 'bill/client_update.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('client_table')
        return form


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'bill/client_delete.html'
    def get_success_url(self):
        self.success_url = reverse('client_table')


class ClientFacturesListView(DetailView):
    template_name = 'bill/client_factures_list.html'
    model = Client

    def get_context_data(self, **kwargs):
        context = super(ClientFacturesListView, self).get_context_data(**kwargs)
        queryset = Facture.objects.filter(client_id=self.kwargs.get('pk')).annotate(total=Sum(
            ExpressionWrapper(F('lignes__qte'), output_field=FloatField()) * F('lignes__produit__prix')))
        table = FactureTable(queryset)
        context['table'] = table
        return context


class FactureTable(tables.Table):
    class Meta:
        model = Facture
        template_name = "django_tables2/bootstrap4.html"
        fields = ('id', 'date','total')


class FactureCreateView(CreateView):
    model = Facture
    template_name = 'bill/create_facture.html'
    fields = ['client', 'date']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.fields['client'] = forms.ModelChoiceField(
            queryset=Client.objects.filter(id=self.kwargs.get('client_pk')), initial=0)
        form.fields['date'] = forms.DateField(
        widget=DatePickerInput(format='%m/%d/%Y')
    )
        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('client_factures_list', kwargs={'pk': self.kwargs.get('client_pk')})
        return form

class FournisseurTable(tables.Table):
    action = '<a href="{% url "fournisseur_update" pk=record.id %}" class="btn btn-warning">Modifier</a>\
              <a href="{% url "fournisseur_delete" pk=record.id %}" class="btn btn-danger">Supprimer</a>'
    edit = tables.TemplateColumn(action)
    
    class Meta:
        model = Fournisseur
        template_name = "django_tables2/bootstrap4.html"
        fields = ('designation', 'adresse')


class FournisseursView(ListView):
    model = Fournisseur
    template_name = 'bill/fournisseur_table.html'

    def get_context_data(self, **kwargs):
        context = super(FournisseursView, self).get_context_data(**kwargs)

        queryset = Fournisseur.objects.all()
        table = FournisseurTable(queryset)
        RequestConfig(self.request, paginate={"per_page": 10}).configure(table)
        context['table'] = table
        return context


class FournisseurCreateView(CreateView):
    model = Fournisseur
    template_name = 'bill/create_fournisseur.html'
    fields = ['designation', 'adresse']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()


        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('fournisseur_table')
        return form

class FournisseurUpdateView(UpdateView):
    model = Fournisseur
    fields = ['designation', 'adresse']
    template_name = 'bill/fournisseur_update.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('fournisseur_table')
        return form


class FournisseurDeleteView(DeleteView):
    model = Fournisseur
    fields = ['designation', 'adresse']
    template_name = 'bill/fournisseur_delete.html'

    def get_success_url(self):
        self.success_url = reverse('fournisseur_table')


class CAClientTable(tables.Table):
    class Meta:
        model = Client
        template_name = "django_tables2/bootstrap4.html"
        fields = ('chiffre_affaire','nom', 'prenom' )


class CAFournisseurTable(tables.Table):
    class Meta:
        model = Fournisseur
        template_name = "django_tables2/bootstrap4.html"
        fields = ('chiffre_affaire','designation', 'adresse' )


class DashboardTables(MultiTableMixin, TemplateView):
    template_name = 'bill/dashboard.html'
    table_pagination = {
        "per_page": 10
    }

    def get_tables(self):
        qs1=  Fournisseur.objects.values('designation', 'adresse').annotate(chiffre_affaire=Sum(
            ExpressionWrapper(F('produits__factures__qte'), output_field=FloatField()) * F(
                'produits__prix')))
        qs2= Client.objects.values('nom', 'prenom').annotate(chiffre_affaire=Sum(
            ExpressionWrapper(F('facture__lignes__qte'), output_field=FloatField()) * F(
                'facture__lignes__produit__prix'))).order_by('-chiffre_affaire')
        return [
            CAFournisseurTable(qs1),
            CAClientTable(qs2)
        ]


def signup(request):
    if request.method == 'POST':
        form =  UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'bill/signup.html', {'form': form})


class ProduitTable(tables.Table):
    action = '<a href="{% url "YOUR_VIEW_DEF" pk=record.id %}" class="btn btn-warning">Ajouter au panier</a>'
    edit = tables.TemplateColumn(action)

    class Meta:
        model = Produit
        template_name = "django_tables2/bootstrap4.html"
        fields = ('photo','designation', 'prix','fournisseur')


class ProduitsView(ListView):
    model = Produit
    template_name = 'bill/produits_table.html'

    def get_context_data(self, **kwargs):
        context = super(ProduitsView, self).get_context_data(**kwargs)

        queryset = Produit.objects.all()
        table = ProduitTable(queryset)
        context['table'] = table
        return context

def YOUR_VIEW_DEF(request, pk):
    panier = request.session.get("panier")
    if panier is None:
        panier = []
    panier.append(PanierLine(pk,1).serialize())
    request.session["panier"] = panier
    #pan = request.session.get("panier")
    return redirect('produits_table')
    """
    if pan is not None:
        print(pan[0])
    """

class PanierTable(tables.Table):
    class Meta:
        model = Produit
        template_name = "django_tables2/bootstrap4.html"
        fields = ('photo','designation','qte','prix')


class PanierView(ListView):
    model = Produit
    template_name = 'bill/panier_table.html'

    def get_context_data(self, **kwargs):
        context = super(PanierView, self).get_context_data(**kwargs)

        queryset = Produit.objects.all()
        table = ProduitTable(queryset)
        context['table'] = table
        return context

