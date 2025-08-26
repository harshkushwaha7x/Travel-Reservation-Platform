from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # normalize the email by making it lowercase
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    image  = models.ImageField(upload_to='images/', null=True, default='images/default_user.jfif')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

class Categorie(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', null=True)


class Promotion(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()
    remise = models.DecimalField(
        max_digits=3, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()

class Offre(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images/', null=True)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True)
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True)
    capacite = models.IntegerField(default=1)
    lieu = models.CharField(max_length=200, default="")
    is_active = models.BooleanField(default=True)


class Reservation(models.Model):
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    nombre_personnes = models.IntegerField(default=1)
    prix = models.FloatField(default=1)

class Notification(models.Model):
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
class Message(models.Model) :
    email = models.EmailField()
    message = models.TextField()
    name = models.CharField(max_length=50)
# Create your models here.
