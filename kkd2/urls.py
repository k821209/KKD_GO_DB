from django.conf.urls import url
from . import views
urlpatterns = [
  url(r'^GO_enrich/',views.do_go_enrich, name='go_enrich'),
  url(r'^$',views.index, name='index'),
  url(r'^detail/(?P<s_id>.+)/$', views.detail_go_enrich, name='detail'),
  url(r'^detail_gene/(?P<s_user>.+)/(?P<s_title>.+)/(?P<s_id_go>.+)/$', views.detail_go_genes, name='detail_gene'), 
]

