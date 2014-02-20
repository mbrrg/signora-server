from django.db import models


class ModelBase(models.Model):
    created = models.DateTimeField('created at', editable=False, auto_now_add=True)
    modified = models.DateTimeField('last modified', editable=False, auto_now=True)

    class Meta:
        abstract = True
        ordering = ('created', 'modified',)


class Device(ModelBase):
    identifier = models.CharField(max_length=128, unique=True, editable=False)
    location = models.CharField(max_length=128, blank=True)
    last_seen = models.DateTimeField('last seen', null=True, editable=False)
    model = models.CharField(max_length=128, editable=False)
    os = models.CharField(max_length=64, null=True, editable=False)
    ip_address = models.GenericIPAddressField(editable=False, null=True)
    app_version = models.CharField(max_length=16, editable=False)

    def __str__(self):
        return (self.location if self.location else 'Unknown location') + ' (' + self.ip_address + ')'


class Weekday(models.Model):
    name = models.CharField(max_length=16)
    iso_weekday = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name


class Schedule(ModelBase):	
    device = models.ForeignKey('Device')
    content = models.ForeignKey('Content')
    valid_days = models.ManyToManyField('Weekday')
    start = models.TimeField()
    end = models.TimeField()


class Content(models.Model):
    SLEEP = 0
    STATIC_URL = 1
    CONTENT_TYPE_CHOICES = (
        (STATIC_URL, 'Static URL'),
        (SLEEP, 'Power save mode'),
    )
    system_content = models.BooleanField(default=False)
    type = models.PositiveIntegerField(choices=CONTENT_TYPE_CHOICES, default=STATIC_URL)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True)
    static_url = models.URLField()

    def __str__(self):
        return self.title
