from django.db import models

# Create your models here.
class GO_enrich(models.Model):
   class Meta:
      db_table = 'go_enrich'
   user   = models.CharField(max_length=20)
   title  = models.CharField(max_length=20)
   GO     = models.CharField(max_length=20)
   Pvalue = models.CharField(max_length=20)
   Odds   = models.CharField(max_length=20)
   name   = models.CharField(max_length=200)
   defin  = models.TextField() 

class subgenes(models.Model):
   class Meta:
      db_table = 'subgenes'
   user   = models.CharField(max_length=20)
   title  = models.CharField(max_length=20)
   Gene_stable_ID      = models.CharField(max_length=20)
   Transcript_stable_ID_version = models.CharField(max_length=20)
   GO_term_accession   = models.CharField(max_length=20)
   GO_term_name        = models.CharField(max_length=20)
   NCBI_gene_ID        = models.CharField(max_length=20)
   GeneID              = models.CharField(max_length=20)
   Gene_name           = models.CharField(max_length=20)
   Gene_description    = models.TextField()	
