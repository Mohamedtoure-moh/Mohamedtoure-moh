from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect, render
from . models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout ,authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
import re
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from enetp import settings
from django.core.mail import send_mail,EmailMessage
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_text
from django.template.loader import render_to_string
from .token import generateur
from .models import *


# Create your views here.
def index(request):
    return render(request, "etudiant/index.html")
#les pages d'acceuil et les ajouts d'etudiants
@csrf_exempt
@login_required
def accueil(request):
    user_id = request.user.id
    annonce = Annonce.objects.all().order_by("-creer")
    return render(request,"etudiant/accueil.html",{
        "user_id":user_id,
        "annonces":annonce
    })
# la fonction qui permet d'ajouter des etudiants
def est_complet(etudiant):
    return all([
        etudiant.nom,
        etudiant.prenom,
        etudiant.date_de_naissance,
        etudiant.lieu_de_naissance,
        etudiant.departement,
        etudiant.filiere,
        etudiant.niveau_de_classe,
        etudiant.carte_fichier.name != "default/path/to/file.pdf",
    ])

def ajouter(request, id):
    user = get_object_or_404(User, pk=id)
    etudiant = Etudiant.objects.filter(user=user).first()

    if etudiant and est_complet(etudiant):
        return render(request, "etudiant/ajouter.html", {
            "etudiant": etudiant,
            "readonly": True,
            "user_id": user.id,
        })

    if request.method == "POST":
        numero_carte = request.POST.get("numero_carte")
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        date_naissance = request.POST.get("date_naissance")
        lieu_naissance = request.POST.get("lieu_naissance")
        niveau = Niveau.objects.get(pk=request.POST.get("niveau"))
        departement = Departement.objects.get(pk=request.POST.get("departement"))
        filiere = Filiere.objects.get(pk=request.POST.get("filiere"))
        carte_etudiant = request.FILES.get("carte_etudiant", None)

        if not etudiant:
            etudiant = Etudiant(user=user)

        etudiant.matricule = numero_carte
        etudiant.nom = nom
        etudiant.prenom = prenom
        etudiant.date_de_naissance = date_naissance
        etudiant.lieu_de_naissance = lieu_naissance
        etudiant.niveau_de_classe = niveau
        etudiant.departement = departement
        etudiant.filiere = filiere
        if carte_etudiant:
            etudiant.carte_fichier = carte_etudiant
        etudiant.save()

        return render(request, "etudiant/ajouter.html", {
            "etudiant": etudiant,
            "success": "Profil mis à jour avec succès.",
            "user_id": user.id,
        })

    return render(request, "etudiant/ajouter.html", {
        "etudiant": etudiant,
        "user_id": user.id,
        "departements": Departement.objects.all(),
        "filieres": Filiere.objects.all(),
        "niveaux": Niveau.objects.all(),
    })
#la partie authentification
def active(request, uidb64, tokens):
    try:
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)
    except(ValueError,User.DoesNotExist, OverflowError, TypeError):
        user = None
    if user is not None and generateur.check_token(user, tokens):
        user.is_active = True
        user.save()
        messages.success(request, 'Compte activé avec succees.')
        return HttpResponseRedirect(reverse("logIn"))
    else:
        messages.error(request, "Erreur d'ctivation de votre compte, veillez reessayer ulterierment.")
        return HttpResponseRedirect(reverse("index"))
def forGet(request):
    if request.method == "POST":
        email = request.POST["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Compte introuvable.")
            HttpResponseRedirect(reverse("index"))
        current_site = get_current_site(request)
        email_subject = "Réinitialisation de votre mot de passe"
        message_email = render_to_string("reinitialisation_mot_de_pass.html", {
            "nom": user.first_name,
            "prenom": user.last_name,
            "domain": current_site.domain,
            "uidb64": urlsafe_base64_encode(force_bytes(user.pk)),
            "tokens": generateur.make_token(user),
            "protocol": "https" if request.is_secure() else "http"
        })
        
        # Envoi de l'email
        mail = EmailMessage(
            email_subject,
            message_email,
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        if mail.send():
            messages.success(request,"Un email vous a été envoyé pour réinitialiser votre mot de pass.")
            return HttpResponseRedirect(reverse("logIn"))
        else:
            messages.error(request, "Erreur d'envoie de email, veillez reesayez.")
            return HttpResponseRedirect(reverse("forGet"))
    else:
        return render(request, "etudiant/forGet.html")
def reset(request, uidb64,tokens):
    try:
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)
    except(ValueError,TypeError, User.DoesNotExist, OverflowError):
        user = None
    if user is not None and generateur.check_token(user,tokens):
        if request.method == "POST":
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]
            if password != confirmation:
                messages.error(request,"Vos mot de pass ne sont pas le meme.")
                return HttpResponseRedirect(reverse("resEt", args=[uidb64,tokens]))
            else:
                user.set_password(password)
                user.save()
                messages.success(request, "Votre mot de passe a été réinitialisé avec succès.")
                return HttpResponseRedirect(reverse("logIn"))
        else:
            #affichage de la page de réinitialisation du mot de passe
            return render(request, "etudiant/resEt.html", {
                "uidb64": uidb64,
                "tokens": tokens,
            })
    else:
        messages.error(request, "Le lien de réinitialisation est invalide ou a expiré.")
        return HttpResponseRedirect(reverse("forGet"))
# la partie footer et contact
def apropos(request):
    return render(request,"etudiant/apropos.html")
def formations(request):
    return render(request, "etudiant/formations.html")
def contact(request):
    return None

#la partie reclamation,transfert et messagerie d'etudiant
@csrf_exempt
@login_required
def reclamation(request, id):
    user = User.objects.get(pk=id)
    try:
        etudiant = Etudiant.objects.get(user=user)
    except Etudiant.DoesNotExist:
        return render(request, "etudiant/reclamation.html", {
            "error": "Étudiant non trouvé pour cet utilisateur.",
            "user_id": id,
        })

    if request.method == "POST":
        sujet = request.POST.get("sujet", "").strip()
        message = request.POST.get("message", "").strip()

        if not sujet or not message:
            return render(request, "etudiant/reclamation.html", {
                "error": "Tous les champs sont requis.",
                "user_id": id,
            })

        try:
            # Assurez-vous de créer la réclamation en utilisant les bons champs
            reclamation = Reclamation(
                sujet=sujet,
                message=message,
                etudiant=etudiant,
            )
            reclamation.save()

            # Redirection vers la messagerie avec un message de succès
            return redirect('messagerie',id=id)

        except Exception as e:
            return render(request, "etudiant/reclamation.html", {
                "error": f"Une erreur est survenue : {str(e)}",
                "user_id": id,
            })

    return render(request, "etudiant/reclamation.html", {
        "user_id": id,
    })

@csrf_exempt
@login_required
def transfert(request):
    return render(request,"etudiant/transfert.html")
def messagerie(request, id):
    try:
        user = User.objects.get(pk=id)
        etudiant = Etudiant.objects.get(user=user)
    except (User.DoesNotExist, Etudiant.DoesNotExist):
        return render(request, "etudiant/messagerie.html", {
            "error": "Étudiant ou utilisateur non trouvé.",
            "user_id": id,
        })

    reclamations = Reclamation.objects.filter(etudiant=etudiant)
    messages = Messagerie.objects.filter(etudiant=etudiant)

    success_message = request.GET.get('success', None)

    return render(request, "etudiant/messagerie.html", {
        "messages": messages,
        "reclamations": reclamations,
        "user_id": id,
        "success_message": success_message,
    })
def message(request, id):
    user = User.objects.get(pk=id)
    try:
        etudiant = Etudiant.objects.get(user=user)
    except Etudiant.DoesNotExist:
        return render(request, "etudiant/message.html", {
            "error": "Étudiant non trouvé pour cet utilisateur.",
            "user_id": id,
        })

    if request.method == "POST":
        sujet = request.POST.get("sujet", "").strip()
        contenu = request.POST.get("contenu", "").strip()

        if not sujet or not contenu:
            return render(request, "etudiant/message.html", {
                "error": "Tous les champs sont requis.",
                "user_id": id,
            })

        try:
            message = Messagerie(
                sujet=sujet,
                contenu=contenu,
                etudiant=etudiant,
            )
            message.save()
            return redirect('messagerie',id=id)

        except Exception as e:
            return render(request, "etudiant/message.html", {
                "error": f"Une erreur est survenue : {str(e)}",
                "user_id": id,
            })

    return render(request, "etudiant/message.html", {
        "user_id": id,
    })

#la fonction permettant de renforcer la securité du mot de pass
def is_password_strong(password):
    if len(password) < 8:
        return "Le mot de passe doit contenir au moins 8 caractères."
    if not any(char.isupper() for char in password):
        return "Le mot de passe doit contenir au moins une lettre majuscule."
    if not any(char.isdigit() for char in password):
        return "Le mot de passe doit contenir au moins un chiffre."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Le mot de passe doit contenir au moins un caractère spécial."
    return None
def regIster(request):
    if request.method == "POST":
        nom = request.POST["nom"]
        prenom = request.POST["prenom"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "etudiant/regIster.html",{
                "message":"Mots de pass non identiques"
            })
        #Appel du fonction de securité
        password_error = is_password_strong(password)
        if password_error:
            return render(request, "etudiant/regIster.html", {
                "message": password_error
            })
        try:
            user = User.objects.create_user(email,email,password)
            user.first_name = prenom
            user.last_name = nom
            user.is_active = False
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "etudiant/regIster.html", {
                "message": "Ce email a déjà un compte."
            })
        else:
            #un premier mail de bienvenue
            #sujet du mail.
            subject = "Bienvenue à ENETP"
            # message (contenue du mail).
            message = "Bienvenue " + user.first_name + " " + user.last_name + ",\n\nNous sommes ravis de vous accueillir sur notre plateforme. Vous trouverez ici toutes les ressources nécessaires pour votre parcours.\n\nCordialement,\nL'équipe ENETP"
            #l'expediteur du mail [exemple: no-reply-enetp@enetp.ml].
            from_email = settings.EMAIL_HOST_USER
            #l'expediteur.
            to_email = [user.email]
            #appel du modul importer pour l'envoie du mail.
            send_mail(subject, message, from_email, to_email, fail_silently=True)
            #envoie de mail de confirmation/ouverture du compte
            current_site = get_current_site(request)
            #sujet
            email_subject = "Confirmation d'ouverture de votre compte ENETP"
            #message contenu
            message_confirmation = render_to_string("mail_confirmation.html", {
                "nom": user.first_name,
                "prenom": user.last_name,
                "domain": current_site.domain,
                "uidb64": urlsafe_base64_encode(force_bytes(user.pk)),
                "tokens": generateur.make_token(user),
                "protocol": "https" if request.is_secure() else "http",
            })
            #envoie du mail
            mail = EmailMessage(
                email_subject,
                message_confirmation,
                settings.EMAIL_HOST_USER,
                [user.email]
            )
            mail.fail_silently = True
            mail.send()
            #condition si le mail a ete envoyee
            if mail.send():
                return render(request, "etudiant/logIn.html",{
                    "message":"Merci de consulter votre compte email pour valider la création de votre compte ou vérifier les spams."
                })
            else:
                messages.error("Erreur d'envoie de email, veillez reesayez.")
                return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "etudiant/regIster.html")

def logIn(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        #indication d'un etudiant qui voulez se connecter sans confirmer le mail
        etudiant = User.objects.get(username=email)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("accueil"))
        #elif etudiant.is_active == False:
        #    messages.error(request, "Veillez confirmer votre Email avant de se connecter.")
        #    return HttpResponseRedirect(reverse("logIn"))
        else:
            return render(request,"etudiant/logIn.html",{
                "message":"Mot de pass/ou Identifiant incorrect."
            })
    else:
        return render(request, "etudiant/logIn.html")
@login_required
def logOut(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
