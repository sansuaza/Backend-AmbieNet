# Django rest framework
from rest_framework import serializers

# Models
from AmbieNet.posts.models import AdvancedReport


class AdvancedReportModelSerializer(serializers.ModelSerializer):
    """ AdvancedReportModelSerializer. """

    class Meta:
        """ Meta class. """
        model = AdvancedReport

        fields = (
            'climatic_phenomenon', 'time_interval', 'temp_max',
            'temp_min', 'conditions_can_be_triggered', 'associated_risks'
        )
