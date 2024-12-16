from django.db import models

# Create your models here.


class CommonModel(models.Model):

    """Definition for CommonModel"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
