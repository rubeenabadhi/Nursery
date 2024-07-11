from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField

from account.models import plant_admin


# Create your models here.
class categ_plants(models.Model):
    name=models.CharField(max_length=50,unique=True)
    slug=models.CharField(max_length=50,unique=True)

    def __str__(self):
        return '{}'.format(self.name)

    def get_url(self):
        return reverse('categview', args=[self.slug])



class add_plants(models.Model):
    name=models.CharField(max_length=50,unique=True)
    slug=AutoSlugField(populate_from='name',editable=True, always_update=True)
    img=models.ImageField(upload_to='picture')
    category=models.ForeignKey(categ_plants,on_delete=models.CASCADE)
    price=models.IntegerField()
    details=models.TextField()
    available=models.BooleanField(default=True)
    date=models.DateField(auto_now_add=True)
    stock=models.IntegerField(default=0)
    admin=models.ForeignKey(plant_admin,on_delete=models.CASCADE,default=1,related_name='N_Plants')

    def __str__(self):
        return '{}'.format(self.name)

    @property
    def imageURL(self):   # get image in template
        if self.img:
            return self.img.url


    def get_url(self):
        return reverse('plant_details',args=[self.category.slug,self.slug])
class Feedback(models.Model):
    plant = models.ForeignKey(add_plants, on_delete=models.CASCADE, related_name='review', default='')
    name=models.CharField(max_length=40,unique=True)
    feedback=models.CharField(max_length=500)
    date= models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name

class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    subject=models.CharField(max_length=100)
    message=models.CharField(max_length=1000)
    date=models.DateField(auto_now=True,null=True)
    def __str__(self):
        return self.name
