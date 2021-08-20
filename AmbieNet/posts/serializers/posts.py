"""post sealizer"""
#Django
from django.core.mail import send_mail

# Django REST Framework
from rest_framework import serializers

# Models
from AmbieNet.posts.models import Post, AdvancedReport
from AmbieNet.users.models import User
from AmbieNet.users.models import Profile


# Serializers
from AmbieNet.users.serializers.users import UserModelSerializer
from AmbieNet.posts.serializers.advanced_reports import AdvancedReportModelSerializer


class PostModelSerializer(serializers.ModelSerializer):

    user = UserModelSerializer(read_only=True)
    advanced_report = AdvancedReportModelSerializer(required = False)
    class Meta:
        """Meta Class"""
        model = Post

        fields = (
            'is_banned',
            'title',
            'description',
            'type_catastrophe',
            'latitude',
            'longitude',
            'photo',
            'validator_number',
            'created',
            'id',
            'type_post',
            'user',
            'advanced_report'
        )

        read_only_fields = (
            'title',
            'latitud',
            'longitud',
            'photo',
            'type_catastrophe',
            'created',
            'id',
            'username'
        )

class PostCreateSerializer(serializers.Serializer):

    advanced_report = AdvancedReportModelSerializer(required = False)

    user = serializers.CharField(
        min_length = 1,
        max_length = 50
    )

    type_post = serializers.CharField(max_length = 4)

    photo = serializers.CharField(
        max_length = 255
    )

    title = serializers.CharField(
        min_length = 5,
        max_length = 50
    )

    description = serializers.CharField(
        min_length = 5,
        max_length = 255
    )

    type_catastrophe = serializers.CharField (
        min_length = 2,
        max_length = 20
    )

    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    def create(self, data):
        user = User.objects.get(username=data['user'])
        username = user.username
        profile = Profile.objects.get(user=user)
        data.pop('user')

        if(data['type_post'] == 'ADV'):
            advanced_data = dict(data['advanced_report'])
            advanced_report = AdvancedReport.objects.create(**advanced_data)

            data.pop('advanced_report')

            post = Post.objects.create(
                user=user,
                username=username,
                profile=profile,
                advanced_report = advanced_report,
                **data)
        else:
            post = Post.objects.create(user=user, username=username, profile=profile, **data)

        """making of ubication posts."""
        data= {
            'latitude': post.latitude,
            'longitude': post.longitude
        }
        # self.define_perimeter(data=data)
        self.update_user_punctuation(user = post.user)
        return post

    def update_user_punctuation(self, user):
        """ Handle of increase punctuation of poster user. """
        if user.punctuation < 100:
            if user.punctuation > 95:
                user.punctuation = 100
            else:
                user.punctuation += 5

        user.save()


    def define_perimeter(self, data):
        """Handle of calculate the perimeter of disaster."""
        profiles = Profile.objects.all()
        mails_users_affected = []
        for profile in profiles:
            if(profile.longitude>=(data['longitude'] - 0.000010) and profile.longitude <= (data['longitude'] + 0.000010) and profile.latitude >= (data['latitude'] - 0.000010) and profile.latitude<= (data['latitude'] + 0.000010)):

                subject = 'Mensaje de alerta de castastrofe ambiental cercana'
                message = 'Se le informa que en una locación cerca al lugar donde usted recide, ha ocurrido una catastrofe. Se le recomienda discresión'
                from_email = 'AmbieNet <noreply@ambienet.com>'
                mail = "{}".format(User.objects.get(profile=profile).email)
                send_mail(subject, message, from_email, [mail])
            #mails_users_affected.append(User.objects.get(profile=profile).email)

        #self.send_email_alert(mails= mails_users_affected)

    def send_email_alert(self, mails):
        subject = 'Mensaje de alerta de castastrofe ambiental cercana'
        message = 'Se le informa que en una locación cerca al lugar donde usted recide, ha ocurrido una catastrofe. Se le recomienda discresión'
        from_email = 'AmbieNet <noreply@ambienet.com>'

        users_mails = []
        users_mails = mails
        print('Correos de los usuarios---------------------------------- {}'.format(users_mails))

        datatuple = (subject, message, from_email, [users_mails])
        number_sent_mails = send_mail(subject, message, from_email, [users_mails])

        print('Correos enviados de alerta: ' + str(number_sent_mails))
