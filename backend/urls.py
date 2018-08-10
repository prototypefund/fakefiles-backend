from django.urls import path

from .views import ItemDetailView, ItemListView

urlpatterns = [
    path('', ItemListView.as_view(), name='index'),
    path('<slug>/', ItemDetailView.as_view(), name='item-detail'),
]
