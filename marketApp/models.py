from django.db import models

# Create your models here.
class Organization(models.Model):
    organizationName = models.CharField(max_length=128)
    purpose = models.CharField(max_length=2000)
    emailAddress = models.CharField(max_length=512)
    metaAddress = models.CharField(max_length=64)
    active = models.CharField(max_length=8, default="Y")
    createdDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.id}: organizationName: {self.organizationName} purpose: {self.purpose} emailAddress: {self.emailAddress} metaAddress: {self.metaAddress} active: {self.active} createdDate: {self.createdDate}"

