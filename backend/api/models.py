from django.db import models
from django.contrib.auth.models import User

class GitHubAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    github_username = models.CharField(max_length=255)
    repositories = models.JSONField(default=list, blank=True, null=True)  

    def __str__(self):
        return self.github_username
    
class SelectedRepository(models.Model):
    github_account = models.ForeignKey(GitHubAccount, on_delete=models.CASCADE, related_name='selected_repositories')
    repo_name = models.CharField(max_length=255)
    repo_url = models.URLField()

    def __str__(self):
        return f"{self.repo_name} - {self.repo_url}"