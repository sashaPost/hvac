from django.urls import path
from . import views 



urlpatterns = [
    path(route='case-list/', view=views.case_list, name='case_list'),
    
]