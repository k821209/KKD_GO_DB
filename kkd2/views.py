from django.shortcuts import render
from django import forms
from .models import GO_enrich, subgenes
import networkx
import obonet
import goenrich # https://github.com/jdrudolph/goenrich
import pandas as pd 
from scipy.stats import fisher_exact
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import numpy as np
import textwrap
import matplotlib as mpl
from django.conf import settings
from sqlalchemy import create_engine
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

database_name = settings.DATABASES['default']['NAME']
database_url = 'sqlite:////%s'%database_name
engine = create_engine(database_url, echo=False)


# Create your views here
#
class put_geneset_name(forms.Form):
    user    = forms.CharField(max_length=20)
    title   = forms.CharField(max_length=200)
    geneset = forms.CharField(widget=forms.Textarea)
print (1)
gene2go = goenrich.read.gene2go('/kkd_rnaseq/go_db/gene2go',tax_id=10090) # 10090 : mus musculus, 3702 : arabidopsis thaliana 
graph = obonet.read_obo('/kkd_rnaseq/go_db/go-basic.obo')
#annot = pd.read_csv('/kkd_rnaseq/go_db/GRCm38.o5.GO.GeneID.txt',sep='\t')
annot = pd.read_excel('/kkd_rnaseq/go_db/annotation_mus.xlsx')
# Mus musculus 
ATID     = annot['Gene_stable_ID']
GENEID   = annot['NCBI_gene_ID']
annot['GeneID'] = GENEID
print (2)
dicAT2GD = dict(zip(ATID,GENEID))
dicGD2AT = dict(zip(GENEID,ATID))


def get_go_enrich(sub_genelist):
    sub_genelist_geneid = [dicAT2GD[x] for x in sub_genelist]

    print('total number of query genes : %d'%len(set(sub_genelist)))
    print('total number of query geneids : %d '%len(set(sub_genelist_geneid)))

    id_to_name = {id_: data['name'] for id_, data in graph.nodes(data=True)}
    name_to_id = {data['name']: id_ for id_, data in graph.nodes(data=True)}
    gene2go_ix = gene2go.set_index('GeneID')

    sub_gene2go = gene2go_ix.loc[sub_genelist_geneid]

    target_GO = set(sub_gene2go.dropna()['GO_ID'].values)

    dicGO2P = {'GO':[],
           'Odds':[],
           'Pvalue':[]
          }
    for GO in target_GO:
        x = list(sub_gene2go['GO_ID'].values).count(GO)
        X = len(sub_gene2go['GO_ID'].values) 
        n = list(gene2go['GO_ID'].values).count(GO)
        N = len(gene2go['GO_ID'].values)
        o,p = fisher_exact([[x,n],[X-x,N-n]])
        dicGO2P['GO'].append(GO)
        dicGO2P['Odds'].append(o)
        dicGO2P['Pvalue'].append(p)

    df_go_enrich = pd.DataFrame(dicGO2P)
    def try_else(x,f,key):
        try:
            return f[x][key]
        except KeyError:
            return 'NONE'
    df_go_enrich['defin'] = df_go_enrich['GO'].apply(lambda x : try_else(x,graph.node,'def'))
    df_go_enrich['name'] = df_go_enrich['GO'].apply(lambda x : try_else(x,graph.node,'name'))

    df_go_enrich = df_go_enrich[['GO','Pvalue','Odds','name','defin']]
    m = (df_go_enrich['Odds'] > 1) & (df_go_enrich['Pvalue'] < 0.01)  
    return df_go_enrich[m]

def do_go_enrich(request):
    if request.method == 'POST':
        form = put_geneset_name(request.POST)
        if form.is_valid():
            user  = form.cleaned_data['user']
            title = form.cleaned_data['title']
            query = form.cleaned_data['geneset']
            print(user,title,query)
            #form = put_geneset_name()
            subgenes = list(set([x.strip() for x in query.split('\n')]))
            df = get_go_enrich(subgenes)
            df['user'] = [user for x in range(df.shape[0])]
            df['title'] = [title for x in range(df.shape[0])]
            df.to_sql('go_enrich', engine,if_exists='append',index=False)
            df_annot = annot.set_index('Gene_stable_ID').loc[subgenes].reset_index().dropna()
            df_annot['user'] = [user for x in range(df_annot.shape[0])]
            df_annot['title'] = [title for x in range(df_annot.shape[0])]
            df_annot.to_sql('subgenes',engine,if_exists='append',index=False)
            form = put_geneset_name()
                  
            return render(request, 'kkd2/go_enrich.html', {'form':form})
    else:
        form = put_geneset_name()
        return render(request, 'kkd2/go_enrich.html', {'form':form})

def index(request):
    all_contents = GO_enrich.objects.all()       
    title = [x.title for x in all_contents]
    user  = [x.user  for x in all_contents]
    ID    = [':'.join(x) for x in set(zip(user,title))]
    return render(request, 'kkd2/index.html', {'IDs' : ID})
def detail_go_enrich(request,s_id):
    print(s_id)
    s_user, s_title = s_id.split(':')
    selected_contents = GO_enrich.objects.filter(user=s_user).filter(title=s_title)
    return render(request, 'kkd2/detail_go_enrich.html', {'GOs':selected_contents,'s_id':s_id})

def detail_go_genes(request,s_id_go,s_user,s_title):
    print(s_id_go)
    selected_contents = subgenes.objects.filter(user=s_user).filter(title=s_title).filter(GO_term_accession=s_id_go)
    return render(request, 'kkd2/detail_go_gene.html', {'Genes':selected_contents})
