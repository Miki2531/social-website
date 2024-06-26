from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.contrib.auth.models import User


class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.Case)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    

    def __str__(self):
        return f'Profile of {self.user.username}'


class Contact(models.Model):
    user_form = models.ForeignKey(User, 
                                  related_name='rel_form_set',
                                    on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]

        ordering = ['-created']

    def __str__(self) -> str:
        return f"{self.user_form} follows {self.user_to}"
    
user_model = get_user_model()
user_model.add_to_class('following', models.ManyToManyField('self', 
                                                            through=Contact,
                                                            related_name='followers',
                                                            symmetrical=False))