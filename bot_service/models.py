from django.db import models


class Album(models.Model):
    name = models.CharField(max_length=100,default='', null=True)
    video = models.FileField('video', upload_to='videos/', null=True)
    gif = models.FileField('gif', upload_to='gifs/', null=True)


    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, default='', null=True)
    id = models.IntegerField('Product Code', primary_key=True, default=False, null=False)
    image = models.ImageField(upload_to='image/', null=True)
    stock = models.IntegerField(default=0, null=True)

    def __int__(self):
        return self.id


class Order(models.Model):
    product = models.ForeignKey(Product, default=False,on_delete=models.CASCADE)
    date = models.DateTimeField(default=False, null=True)
    number = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.product + self.date


class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=50 ,default=False, null=False)
    order = models.ManyToManyField(Order)

    class Meta:
        ordering = ['user_id']

    def __str__(self):
        return self.user_id


class Visit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(default=False, null = True)
    counter = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.product + self.counter


class Admin(models.Model):
    user_id = models.CharField(max_length=50, default=True, null=True )

    def __str__(self):
        return self.user_id


class ChannelPost(models.Model):
    image = models.ImageField(upload_to='post/image/', null=True)
    Description = models.TextField(default=False, null=True)
    Post_time = models.DateTimeField(default=False,null=True)
