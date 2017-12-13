from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add_hierarchy$',views.add_hierarchy, name='add_hierarchy'),
    url(r'^add_designation$',views.add_designation, name='add_designation'),
    url(r'^show_hierarchy$',views.show_hierarchy, name='show_hierarchy'),
    ]
