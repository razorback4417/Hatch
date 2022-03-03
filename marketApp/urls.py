from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("createNFT", views.createNFT, name="createNFT"),
    path("connect", views.connect, name="connect"),
    path("nfts", views.nfts, name="nfts"),
    path("mynft", views.mynft, name="mynft"),
    path("nfts/<int:id>/", views.list_market, name="list_market")
]