from django.urls import  path, re_path, include
from app import views
urlpatterns = [
    re_path(r'^facture_detail/(?P<pk>\d+)/$', views.facture_detail_view, name='facture_detail'),
    re_path(r'^facture_table/(?P<pk>\d+)/$', views.FactureDetailView.as_view(), name='facture_table')

]