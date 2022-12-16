from django.db import models
from  test5mm import settings



class Category(models.Model):
    title = models.CharField(max_length=200, db_index=True)

    def __str__(self):
        return self.title


class Watch(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    price = models.IntegerField(default=0)
    image = models.URLField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



class Photo(models.Model):
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField()

    def __str__(self):
        return self.watch.title + ' photo'


class Review(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=255)
    stars = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.author.__str__() + ' ' + self.title