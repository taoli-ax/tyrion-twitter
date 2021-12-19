from rest_framework import serializers
from tweets.models import Tweet
from accounts.api.serializers import UserSerializerForTweet


class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializerForTweet()

    class Meta:
        model = Tweet
        fields = ('user', 'content', 'created_at')


class TweetSerializerForCreateTweet(serializers.ModelSerializer):
    content = serializers.CharField(min_length=1,max_length=100)

    class Meta:
        model = Tweet
        fields = ('content',)

    def create(self, validated_data):
        user = self.context['user']
        content = validated_data['content']
        tweet = Tweet.objects.create(user=user,content=content)
        return tweet

