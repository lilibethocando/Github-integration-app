from rest_framework import serializers

class GitHubTokenSerializer(serializers.Serializer):
    code = serializers.CharField()
    



class RepositorySelectionSerializer(serializers.Serializer):
    repo_id = serializers.IntegerField()
