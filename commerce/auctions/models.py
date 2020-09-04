from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    watchlist = models.ManyToManyField('Listing', related_name='watchers')


class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    active = models.BooleanField(default=True)

    img_url = models.URLField(blank=True, null=True)
    highest_bid = models.DecimalField(
        decimal_places=2, max_digits=10, default=0)
    winner = models.OneToOneField(
        'User', on_delete=models.CASCADE, blank=True, null=True)

    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='listings')
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name='listings')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ${self.price} by {self.user}, {self.active}"


class Bid(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=10)

    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='bids')
    listing = models.ForeignKey(
        'Listing', on_delete=models.CASCADE, related_name='bids')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} by {self.user} at {self.created_at}"


class Comment(models.Model):
    body = models.TextField()

    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='comments')
    listing = models.ForeignKey(
        'Listing', on_delete=models.CASCADE, related_name='comments')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.body} by {self.user} at {self.created_at}"


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
