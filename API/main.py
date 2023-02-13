from fastapi import FastAPI,Path,UploadFile,File
import pandas as pd
import numpy as np
import io
import boto3

s3_client = boto3.client('s3',
    aws_access_key_id = 'AKIA5B256M6M4Z6LAAHE',
    aws_secret_access_key = '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',
    region_name = 'us-east-1')

session = boto3.Session(aws_access_key_id='AKIA5B256M6M4Z6LAAHE', aws_secret_access_key='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')
s3 = session.resource('s3')
my_bucket = s3.Bucket('datos-trabajados-databrew')
dataframes = []
for my_bucket_object in my_bucket.objects.all():
    key = my_bucket_object.key
    nombre = key.split('/')[1]
    print(f'cargando {nombre}')
    response = s3_client.get_object(Bucket='datos-trabajados-databrew',Key=key)
    data = response['Body'].read()  
    pq_file = io.BytesIO(data)
    df = pd.read_parquet(pq_file)
    dataframes.append({nombre:df})

# closed_deals = dataframes[0]['closed-deals']
# custumers = dataframes[1]['custumers']
# marketing = dataframes[2]['marketing']
# order_items = dataframes[3]['order-items']
# order_sellers = dataframes[4]['sellers']
order_delivered = dataframes[5]['order-sin-nulos']
# payment_sequentel = dataframes[6]['payment']
# products = dataframes[7]['products']
# reviews = dataframes[8]['reviews']
orders_No_delivered = dataframes[9]['Order-nulos-lau']
# conexiones_X_estado = dataframes[10]['conectividad']
# geolocation = dataframes[11]['geolocation']

app = FastAPI(title='Olist')

@app.get('/devolver una tabla/')
async def get_max_duration(nombre:str):
    for data in dataframes:
        key_dicc =list(data.keys())[0]
        if nombre == key_dicc :
            data_to_return = data[key_dicc]
    
    return {data_to_return.to_csv()}

@app.get('/devolver un producto/')
async def get_max_duration(tipo:str):
    df = dataframes[7]['products']
    data = df.loc[df['product_category_name'] == tipo]
    
    return {data.to_json()}

@app.get('/puntaje por producto/')
async def get_max_duration(prod_id:str):
    orders = pd.concat([orders_No_delivered,order_delivered])
    df = pd.merge(dataframes[8]['reviews'],orders,on ='order_id')
    df = pd.merge(df,dataframes[3]['order-items'],on='order_id')
    data = df.loc[df['product_id'] == prod_id]
    if data.empty:
        return {'este producto no existe o no tiene ventas'}
    
    prom = data['review_score'].mean()
    return {'el puntaje promedio es ' : round(prom,1)}

# cargando closed-deals
# cargando custumers
# cargando marketing
# cargando order-items
# cargando sellers
# cargando order-sin-nulos
# cargando payment
# cargando products
# cargando reviews
# cargando Order-nulos-lau
# cargando conectividad
# cargando geolocation