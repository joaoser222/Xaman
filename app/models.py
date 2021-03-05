from django.db.models import *
from django.core.validators import *
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

#Classe que contém as regras de negócio do usuário 
class UserManager(BaseUserManager):
  use_in_migrations = True

  def _create_user(self, email, password, **extra_fields):
    """
    Creates and saves a User with the given email and password.
    """
    if not email:
      raise ValueError('The given email must be set')
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password=None, **extra_fields):
    extra_fields.setdefault('is_superuser', False)
    return self._create_user(email, password, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    extra_fields.setdefault('is_superuser', True)

    if extra_fields.get('is_superuser') is not True:
      raise ValueError('Superuser must have is_superuser=True.')

    return self._create_user(email, password, **extra_fields)

# Mixin com timestamps
class Base(Model):
  created_at = DateTimeField(auto_now_add=True)
  updated_at = DateTimeField(auto_now=True)
  objects = Manager()
  class Meta:
    abstract = True

# Classe de usuários do sistema
class User(AbstractBaseUser, PermissionsMixin, Base):
  email = EmailField(_('email address'), unique=True)
  name = CharField(
    max_length=50,
    null=False,
    blank=False,
  )
  @property
  def username(self):
    return self.nickname
  @property
  def date_joined(self):
    return self.created_at
  is_active = BooleanField(_('active'), default=True)
  avatar = ImageField(upload_to='avatars/', null=True, blank=True)
  objects = UserManager()
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []
  class Meta:
    verbose_name = _('user')
    verbose_name_plural = _('users')
  def email_user(self, subject, message, from_email=None, **kwargs):
    # Sends an email to this User.
    send_mail(subject, message, from_email, [self.email], **kwargs)

class Dataset(Base):
  TYPES = (
    ('f', 'File'),
    ('d', 'Database'),
    ('a', 'API'),
  )
  params = TextField(_('params'),null=False,blank=False)
  type = CharField(max_length=1, choices=TYPES)