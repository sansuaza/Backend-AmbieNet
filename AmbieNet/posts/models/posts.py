#Django
from django.db import models

#Utils
from AmbieNet.util.models.ambienet import AmbieNetModel

# Models
from AmbieNet.users.models import User, Profile

class Post(AmbieNetModel):
    """
    Posts.
    Data from common posts of application, (posts of social network).
    """

    """ User's Data. """
    user = models.ForeignKey (User, on_delete = models.CASCADE)
    profile = models.ForeignKey (Profile, on_delete = models.PROTECT)


    """ Kind of Posts. """
    REPORT = 'REP'
    CATASTROPHE = 'CAT'
    POSITIVE_NEWS = 'NEW'
    COMPLAINT = 'COMP'

    TYPE_POST_CHOICES = [
        (REPORT, 'report'),
        (CATASTROPHE, 'catastrophe'),
        (POSITIVE_NEWS, 'positive_news'),
        (COMPLAINT, 'complaint')
    ]

    type_post = models.CharField(
        max_length = 4,
        choices = TYPE_POST_CHOICES,
        blank = False
    )


    """ Kind of Reports. """
    COMMON = 'COM'
    ADVANCED = 'ADV'

    TYPE_REPORT_CHOICES = [
        (COMMON, 'common'),
        (ADVANCED, 'advanced')
    ]

    type_report = models.CharField(
        max_length = 4,
        choices = TYPE_REPORT_CHOICES,
        blank = True
    )

    """ Advanced report relation. """
    advanced_report = models.ForeignKey(
        'posts.AdvancedReport',
        on_delete = models.CASCADE,
        blank = True,
        null = True
    )


    """ Complaint and banning info. """
    cant_user_complaints = models.IntegerField(default = 0)
    is_banned = models.BooleanField(default=False)

    title = models.CharField(max_length=60, blank=False)
    description = models.CharField(max_length=255)
    type_catastrophe = models.CharField(blank=True, max_length=20)
    #"likes"
    validator_number = models.BigIntegerField(default=0)
    photo=models.ImageField(max_length=255, blank=True)
    username = models.CharField(max_length=255, blank=True)

    """ Location Data. """
    #if precision is not exactly change for DecimalField
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    def __str__(self):
        """ Return titles. """
        return self.title
