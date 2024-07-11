from django.db import models
from django.contrib.auth.models import auth,AbstractBaseUser


# Create your models here.
class plant_admin(models.Model):
    name=models.CharField(max_length=50,unique=True,default='Name')
    mob_num=models.CharField(max_length=13,unique=True)
    photo=models.ImageField(upload_to='photos')
    email=models.EmailField()
    password1=models.CharField(max_length=20)
    nursery_address=models.TextField()
    approve=models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.name)

    @property
    def ImageUrl(self):
        if self.photo:
            return self.photo.url
