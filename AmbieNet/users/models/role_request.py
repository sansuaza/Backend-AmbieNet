#Django
from django.db import models

#Utils
from AmbieNet.util.models.ambienet import AmbieNetModel
from AmbieNet.users.models import User

class RoleRequest(AmbieNetModel):
    """role_request model."""

    """Related users."""
    requesting_user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = 'role_request')

    staff_validator_username = models.CharField(blank = True, max_length = 10)

    new_role = models.PositiveSmallIntegerField(
        help_text= 'Role requested by an user',
        default= 0
        )

    """Request status."""
    PENDING = 1
    REJECTED = 2
    APPROVED = 3

    STATUS_CHOICES = (
        (PENDING, 'pending'),
        (REJECTED, 'rejected'),
        (APPROVED, 'approved')
    )

    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, blank=True, null=True, default=1)

    message = models.TextField(blank = True)
