from django.urls import path
from App_House.views import *

app_name = 'App_House'

urlpatterns = [
    path('create-owner/', createOwner, name='createOwner'),
    path('open-lock/', lockOpen, name='lockOpen'),
    path('lock-close/', lockClose, name='lockClose'),
    path('inside/', insideHouse, name='insideHouse'),
    path('outside/', outsideHouse, name='outsideHouse'),
    path('alert/', alert, name='alert'),
    path('change-password/', change_password, name='change_password'),
]
