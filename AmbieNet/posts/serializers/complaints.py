# Django REST Framework
from rest_framework import serializers

# Serializers
from AmbieNet.users.serializers.users import UserModelSerializer
from AmbieNet.posts.serializers import PostModelSerializer

# Model
from AmbieNet.posts.models import PostComplaint

class PostComplaintModelSerializer(serializers.ModelSerializer):

    reporting_user = UserModelSerializer(read_only = True)
    reported_post = PostModelSerializer(read_only = True)

    class Meta:
        model = PostComplaint
        fields = ['reporting_user', 'reported_post']


    def validate(self, data):

        post_complaint = PostComplaint.objects.filter(
            reporting_user = self.context['reporting_user'],
            reported_post = self.context['reported_post']
        )

        if post_complaint.exists():
            raise serializers.ValidationError('This user has already reported this post.')

        return data

    def create(self, data):
        user = self.context['reporting_user']
        post = self.context['reported_post']

        post_complaint = PostComplaint.objects.create(
            reporting_user = user,
            reported_post = post
        )

        # User quantity reports update
        post.cant_user_complaints += 1
        post.save()

        # check if the post has to be banned
        if not post.cant_user_complaints < 20:
            post.is_banned = True
            self.update_punctuation_user(post.user)
            post.save()

        return post_complaint

    def update_punctuation_user(self, user):
        """ Update the user punctuation after bann a post """

        user.punctuation -= 10
        user.check_level()
        user.save()

        return user
