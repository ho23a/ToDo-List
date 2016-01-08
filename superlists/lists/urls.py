from django.conf.urls import include, url
from lists import views

urlpatterns = [
    url(r'^new$', views.new_list, name="new_list"), #no slash for POST
    url(r'^(\d+)/add_item$', views.add_item, name="add item"),
    # (): capture group, \d: only match digits, .: any character
    url(r'^(\d+)/$', views.view_list, name="view_list"),

]
