from django.db import models
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'


class Stock(models.Model):
    category = models.ForeignKey(
        Category, max_length=50, null=True, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=50, null=True)
    quantity = models.IntegerField(default='0', null=True)
    receive_quantity = models.IntegerField(
        default='0', blank=True, null=True)
    receive_by = models.CharField(max_length=50, blank=True, null=True)
    issue_quantity = models.IntegerField(
        default='0', blank=True, null=True)
    issue_by = models.CharField(max_length=50, blank=True, null=True)
    issue_to = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    export_to_CSV = models.BooleanField(default=False)

    def __str__(self):
        return str(self.item_name)

    # def get_absolute_url(self, ):
    #     return reverse('item_details', kwargs={
    #         'pk': self.pk, })
