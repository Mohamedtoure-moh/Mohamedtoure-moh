from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    #1s parts 
    path("", views.index, name="index"),
    path("register",views.regIster,name="regIster"),
    path("login",views.logIn,name="logIn"),
    path("logout",views.logOut,name="logOut"),
    path("accueil",views.accueil,name="accueil"),
    path("active/<str:uidb64>/<str:tokens>", views.active, name="active"),
    path("forGet",views.forGet,name="forGet"),
    path("reset/<str:uidb64>/<str:tokens>", views.reset, name="reset"),
# Api routes

    #Api logout -- connextion not necessaire
    #path("apropos",views.apropos,name="aprOpos"),
    #path("formations",views.formations,name="forMations"),
    #path("contact", views.contact,name="conTact"),

    # Api login -- connextion neccessaire
    path("completez/<int:id>",views.ajouter,name="ajouter"),
    ## path("transfert",views.transfert,name="transfert"),
    path("reclamation/<int:id>",views.reclamation,name="reclamation"),
    path("messagerie/<int:id>",views.messagerie,name="messagerie"),
    path('message/<int:id>/', views.message, name='message'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)