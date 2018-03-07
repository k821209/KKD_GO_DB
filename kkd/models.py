from django.db import models

class GO(models.Model):
   class Meta:
      db_table = 'go'
   GO     = models.CharField(max_length=20)
   Pvalue = models.CharField(max_length=20)
   Odds   = models.CharField(max_length=20)
   name   = models.CharField(max_length=200)
   defin  = models.TextField() 
   

# Create your models here.
