#action predefinie avec django
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#mail utiliser == gmail
EMAIL_HOST = 'smtp.gmail.com'
#port utiliser pour les tls
EMAIL_PORT = 587
EMAIL_USE_TLS = True
#adress qui doit envoyer le mail exples = [no-replay-enetp@enetp.ml] 
EMAIL_HOST_USER = 'mamato7944@gmail.com'
#mot de pass generer dans securiter google
EMAIL_HOST_PASSWORD = 'ucginjoryhdyjnud '
#defeaut : adress qui doit envoyer le mail exples = [no-replay-enetp@enetp.ml] 
DEFAULT_FROM_EMAIL = 'mamato7944@gmail.com'
