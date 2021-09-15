# Django
from django.db import models

#Utils
from AmbieNet.util.models.ambienet import AmbieNetModel

# Models
from AmbieNet.users.models import User
from AmbieNet.posts.models import Post

class PostComplaint(AmbieNetModel):
    """
    Model to make a complaint to posts that has inappropiate content.
    """

    reporting_user = models.ForeignKey (User, on_delete = models.CASCADE)
    reported_post = models.ForeignKey (Post, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.reporting_user.username} reports {self.reported_post} post."
