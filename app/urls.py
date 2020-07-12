from django.urls import  path, re_path, include
from app import views
urlpatterns = [
    re_path(r'^facture_detail/(?P<pk>\d+)/$', views.facture_detail_view, name='facture_detail'),
    re_path(r'^facture_table_detail/(?P<pk>\d+)/$', views.FactureDetailView.as_view(), name='facture_table_detail'),
    re_path(r'^facture_table_create/(?P<facture_pk>\d+)/$', views.LigneFactureCreateView.as_view(), name='facture_table_create'),
    re_path(r'^lignefacture_delete/(?P<pk>\d+)/(?P<facture_pk>\d+)/$', views.LigneFactureDeleteView.as_view(), name='lignefacture_delete'),
    re_path(r'^lignefacture_update/(?P<pk>\d+)/(?P<facture_pk>\d+)/$', views.LigneFactureUpdateView.as_view(), name='lignefacture_update'),
    re_path(r'^facture_update/(?P<pk>\d+)/$', views.FactureUpdate.as_view(), name='facture_detail'),
    re_path(r'^client_table/$', views.ClientsView.as_view(), name='client_table'),
    re_path(r'^client_create/$', views.ClientCreateView.as_view(), name='client_create'),
     re_path(r'^client_delete/(?P<pk>\d+)/$', views.ClientDeleteView.as_view(), name='client_delete'),
    re_path(r'^client_update/(?P<pk>\d+)/$', views.ClientUpdateView.as_view(),  name='client_update'),
    re_path(r'^client_factures_list/(?P<pk>\d+)/$', views.ClientFacturesListView.as_view(),  name='client_factures_list'),
    re_path(r'^facture_create/(?P<client_pk>\d+)/$', views.FactureCreateView.as_view(), name='facture_create'),
    re_path(r'^fournisseur_table/$', views.FournisseursView.as_view(), name='fournisseur_table'),
    re_path(r'^fournisseur_create/$', views.FournisseurCreateView.as_view(), name='fournisseur_create'),
    re_path(r'^fournisseur_delete/(?P<pk>\d+)/$', views.FournisseurDeleteView.as_view(), name='fournisseur_delete'),
    re_path(r'^fournisseur_update/(?P<pk>\d+)/$', views.FournisseurUpdateView.as_view(),  name='fournisseur_update'),
    re_path(r'^dashboard/$', views.DashboardTables.as_view(),  name='dashboard'),
    re_path(r'^signup/$', views.signup, name='signup'),

    re_path(r'^produits/$', views.ProduitsView.as_view(), name='produits_table'),
    re_path(r'^YOUR_VIEW_DEF/(?P<pk>\d+)$', views.YOUR_VIEW_DEF, name='YOUR_VIEW_DEF'),


]