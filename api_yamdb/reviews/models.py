from django.db import models


class Comment(models.Model):
    rewiew = models.ForeigKey('Rewiew', on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)


class Rewiew(models.Model):
    title = models.ForeignKey('Title', on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    score = models.IntegerField(blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
