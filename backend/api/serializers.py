from rest_framework import serializers

class SocialSerializer(serializers.Serializer):
    access_token = serializers.CharField()
