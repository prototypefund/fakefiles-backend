from django.urls import path

from .admin_views import ItemCreateView
from .views import ItemDetailView, ItemListView

urlpatterns = [
    path('', ItemListView.as_view(), name='index'),
    path('new/', ItemCreateView.as_view(), name='item-create'),
    path('<slug>/', ItemDetailView.as_view(), name='item-detail'),
]
