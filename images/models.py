from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

class Image(models.Model):
    user = models.ForeignKey(User, related_name='image_created', on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name='images_liked', blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    url = models.URLField(max_length=2000)
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        
        ordering = ['created']
    

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])
    
