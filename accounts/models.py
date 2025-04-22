from django.db import models
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser, 
                                        PermissionsMixin,
                                        Group,
                                        Permission)
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator, RegexValidator
from uuid import uuid4

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, phone=None, password=None, **extra_fields):
        if not(email or phone):
            raise ValueError(_("Email or phone is required."))
        
        if not username:
            username = email.split('@')[0] if email else f"user_{str(uuid4())[:8]}"
        
        email = self.normalize_email(email) if email else None
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        user = self.model(username = username,email = email,phone = phone,**extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, username, email=None, phone=None, password=None, **extra_fields):
        if not(email or phone):
            raise ValueError(_("Super user must have an email or phone."))
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have is_staff = True."))
        
        if extra_fields.get('is_superuser') is not True :
            raise ValueError(_("Superuser must have is_superuser = True."))
        return self.create_user(username=username, email=email, phone=phone, password=password, **extra_fields)

        

class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Autnetication fields
    username = models.CharField(max_length=30, unique= True, validators=[MinLengthValidator(4)])
    email = models.EmailField(max_length=50, unique=True, blank= True, null=True)
    phone = models.CharField(max_length=20, unique=True, blank=True, null= True,validators=[RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Enter a valid phone no. (eg. +9779874882832)."
    )])
    
    # Authorization fields
    is_staff = models.BooleanField(default=False) # For admin access
    is_active = models.BooleanField(default=True) # For account activation/deactivation

    objects = CustomUserManager()

    USERNAME_FIELD = "username" #Default identifier (for 'createsuperuser')
    REQUIRED_FIELDS = ["email"] # No extra prompts (email/phone handled in manager)
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_set",  
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions', 
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",  
        related_query_name="user",
    ) 

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(email__isnull = False) | models.Q(phone__isnull = False),
                name = "require_email_or_phone"
            )
        ]

    def __str__(self):
            return self.username
        
    def save(self, *args, **kwargs):
            self.username = self.username.lower() #Case insensitive username
            super().save(*args, **kwargs)