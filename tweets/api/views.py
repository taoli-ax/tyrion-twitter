from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from tweets.models import Tweet
from tweets.api.serializers import TweetSerializer,TweetSerializerForCreateTweet



class TweetViewSet(viewsets.ModelViewSet):
    serializer_class = TweetSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        if 'user_id' not in request.query_params:
            return Response('missing user id',status=400)
        tweets = Tweet.objects.filter(user_id=request.query_params['user_id']).order_by('-created_at')
        serializer = TweetSerializer(tweets,many=True)
        return Response({'tweets': serializer.data})

    def create(self, request, *args, **kwargs):
        serializer = TweetSerializerForCreateTweet(data=request.data,context={'user':request.user})
        if not serializer.is_valid():
            return Response({
                'success':False,
                'message':'Please check input.'
            },status=400)
        tweet = serializer.save()
        return Response({
            'success':True,
            'tweet':TweetSerializer(tweet).data
        })