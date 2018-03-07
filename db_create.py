import pandas as pd
from django.conf import settings
from sqlalchemy import create_engine
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

database_name = settings.DATABASES['default']['NAME']
database_url = 'sqlite:////%s'%database_name
engine = create_engine(database_url, echo=False)
df_django = pd.read_csv('GO_list.txt',sep='\t')
df_django.to_sql('go', engine,if_exists='append',index=False)
