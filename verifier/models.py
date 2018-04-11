from django.db import models


class Website(models.Model):
    url = models.CharField(max_length=100)
    id_tag = models.CharField(max_length=100)
    content = models.CharField(max_length=200)
    time = models.TimeField(null=True)
    code = models.IntegerField(null=True)
    result = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return self.url

    def __str__(self):
        return '%s' % (self.url)
