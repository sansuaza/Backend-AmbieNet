# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
# Utils
from AmbieNet.util.models.ambienet import AmbieNetModel


class User(AmbieNetModel, AbstractUser):
    """ User model
    Extends from AbstractUser, and keeps the same usernamefield (username).
    """

    ENTIDAD = 1
    SENSOR_SOCIAL = 2
    USUARIO_REGULAR = 3

    ROLE_CHOICES = (
        (ENTIDAD, 'entidad'),
        (SENSOR_SOCIAL, 'sensor_social'),
        (USUARIO_REGULAR, 'usuario_regular')
    )

    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES,
        blank=True,
        null=True,
        default=3
        )

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        }
    )

    phone_regex = RegexValidator(

        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)


    REQUIRED_FIELDS = ['first_name', 'last_name']

    """ All users get verified by email message. """
    is_verified = models.BooleanField(
        'verified',
        default=True,
        help_text='Set to true when the user have verified its email address.'
    )

    """ Reputation Info. """
    quantity_reported_posts = models.IntegerField(default = 0)
    punctuation = models.IntegerField(default = 0)
    level = models.SmallIntegerField(default = 0)

    def __str__(self):
        """Return username."""
        return self.username

    def get_short_name(self):
        """Return username."""
        return self.username

    def check_level(self):
        LEVEL_2 = 20
        LEVEL_3 = 35
        LEVEL_4 = 60
        LEVEL_5 = 100

        if self.punctuation < LEVEL_2:
            self.level = 1
        elif self.punctuation < LEVEL_3:
            self.level = 2
        elif self.punctuation < LEVEL_4:
            self.level = 3
        elif self.punctuation < LEVEL_5:
            self.level = 4
        elif self.punctuation == LEVEL_5:
            self.level = 5

        return self.level
