from django.db import models

class Book(models.Model):
    oldLatynUrl = models.CharField(max_length=255)
    speakerId = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    shortDescription = models.TextField()
    thumbnailUrl = models.CharField(max_length=255)
    oldFileUrl = models.CharField(max_length=255)
    filePath = models.CharField(max_length=255)
    hasAudio = models.BooleanField(default=False)
    hasFile = models.BooleanField(default=False)
    language = models.CharField(max_length=255, default='kz')
    year = models.CharField(max_length=255, default='0000')
    addTime = models.PositiveIntegerField()
    updateTime = models.PositiveIntegerField()
    qStatus = models.PositiveSmallIntegerField()
    html = models.TextField()

    def __str__(self):
        return self.title 