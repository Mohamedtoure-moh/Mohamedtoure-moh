from django.contrib import admin
from .models import Departement,Reclamation,Filiere,Etudiant,Annonce,Messagerie,Niveau,User #Transfert

# Register your models here.
admin.site.register(User)
admin.site.register(Departement)
## admin.site.register(Transfert)
admin.site.register(Etudiant)
admin.site.register(Filiere)
admin.site.register(Reclamation)
admin.site.register(Annonce)
admin.site.register(Messagerie)
admin.site.register(Niveau)
