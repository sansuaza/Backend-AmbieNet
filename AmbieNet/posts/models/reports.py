#Django
from django.db import models

#Utils
from AmbieNet.util.models.ambienet import AmbieNetModel

class AdvancedReport(AmbieNetModel):
    """
    Model to persist the info of advanced reports
    """
    climatic_phenomenon = models.CharField(blank = False, max_length = 25)

    time_interval = models.CharField(max_length = 25)
    temp_max = models.FloatField(default = 0.0)
    temp_min = models.FloatField(default = 0.0)

    conditions_can_be_triggered = models.CharField(max_length = 255)
    associated_risks = models.CharField(max_length = 255)

    def __str__(self):
        """ Return titles. """
        return self.climatic_phenomenon
