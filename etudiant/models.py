from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
# La creation des anonnces ou des informations publier par l'administration
class Annonce(models.Model):
    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    fichier = models.FileField(upload_to="annonces/",blank=True,null=True)
    creer = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre}"

class Departement(models.Model):
    nom = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nom

class Filiere(models.Model):
    nom = models.CharField(max_length=255)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, related_name="filieres")

    def __str__(self):
        return self.nom

class Niveau(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="etudiant")
    matricule = models.CharField(max_length=7, unique=True)
    nom = models.CharField(max_length=67)
    prenom = models.CharField(max_length=67)
    date_de_naissance = models.DateField()
    lieu_de_naissance = models.CharField(max_length=200)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, related_name="etudiants", default=1)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name="etudiants")
    niveau_de_classe = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name="etudiants")
    carte_fichier = models.FileField(upload_to="etudiant_files/", default="default/path/to/file.pdf")

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = Etudiant.objects.get(pk=self.pk)
            if old_instance.carte_fichier and old_instance.carte_fichier != self.carte_fichier:
                old_instance.carte_fichier.delete()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.matricule})"

""" class Transfert(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name="transferts")
    ancienne_filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name="transferts_sortants")
    nouvelle_filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name="transferts_entrants")
    date_transfert = models.DateField(auto_now_add=True)
    motif = models.TextField()

    def __str__(self):
        return f"Transfert de {self.etudiant.nom} ({self.ancienne_filiere.nom} -> {self.nouvelle_filiere.nom})" """
    
class Reclamation(models.Model):
    statuts = [ 
        ('en_attente', 'En attente'),
        ('traite', 'Traitée'),
        ('en_cours','En cours'),
        ('rejeté','Rejété')
    ]
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name="etudiants")
    sujet = models.CharField(max_length=255)  # Ajout du champ sujet
    message = models.TextField()
    reponse = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=30, choices=statuts, default="en_attente")
    date_de_soumission = models.DateField(auto_now_add=True)
    date_de_reponse = models.DateField(null=True, blank=True)

    def __str__(self):
        return (f"Departement: {self.etudiant.departement} "
                f"Option: {self.etudiant.filiere} "
                f"Classe/Niveau: {self.etudiant.niveau_de_classe} --> {self.statut}")

class Messagerie(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name="students")
    sujet = models.CharField(max_length=200,null=False, blank=False)
    contenu = models.TextField()
    date_envoie = models.DateField(auto_now_add=True)
    reponse = models.TextField()
    def __str__(self):
        return (f"Departement:{self.etudiant.departement}"
                f" Option:{self.etudiant.filiere}" 
                f"Classe/niveau:{self.etudiant.niveau_de_classe}" 
                f"Nom et Prenom:{self.etudiant.nom} {self.etudiant.prenom}"  
                f"sujet du message: {self.sujet}"
                f"contenue: {self.contenu}"
                f"reponse: {self.reponse}")
    