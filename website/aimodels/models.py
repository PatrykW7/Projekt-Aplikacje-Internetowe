from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files import File

# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length = 255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name
    

class AiModel(models.Model):
    category = models.ForeignKey(Category, related_name = 'aimodels', on_delete = models.CASCADE)
    name = models.CharField(max_length = 255)
    slug = models.SlugField()
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to = 'uploads/', blank = True, null = True)
    thumbnail = models.ImageField(upload_to='uploads/', blank = True, null = True)


    class Meta:
        ordering = ('name', )
    
    # TO BY PODZIALALO DLA SELF.IMAGE ???
    def create_thumbnail(self, image, size = (300, 300)):
        img = Image.open(image)
        img.convert("RGB")
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality = 90)
        
        thumbnail = File(thumb_io, name = image.name)
        return thumbnail


    def get_thumbnail(self):
        if self.image:
            self.thumbnail = self.create_thumbnail(self)
            self.save()
        return self.thumbnail.url

    # WYSWIETLANIE CENY W POPRAWNYM FORMACIE 
    def get_display_price(self):
        return self.price / 100
    

    def __str__(self):
        return self.name