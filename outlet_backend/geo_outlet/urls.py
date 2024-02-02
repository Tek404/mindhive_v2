from django.urls import path
from .views import OutletList, OutletSearchList, search_outlets

urlpatterns = [
    path('outlets/', OutletList.as_view(), name='outlet-list'),
    path('search_outlets/', OutletSearchList.as_view(), name='search-outlet-list'),

    # path('search_outlets/', search_outlets, name='search-outlets'),

]
