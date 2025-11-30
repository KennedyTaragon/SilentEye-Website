from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='clients/', blank=True, null=True)

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    quote = models.TextField()

    def __str__(self):
        return f'Testimonial by {self.name}'