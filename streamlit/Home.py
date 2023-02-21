#Librerías
import streamlit as st
st.set_page_config(page_title="Data Innovative")
import pandas as pd
import numpy as np
import os
from streamlit_option_menu import option_menu

#Título y diseño inicial
st.title(':globe_with_meridians: Data Innovative')
with st.sidebar:
    menu = option_menu(
        menu_title = "Menú",
        options=['Analisis principal, power bi','Machine learning: sistema de recomendaciones'],
        styles={
            "container" : {
                "background-color": "rgba(255, 255, 255, 0) !important",
                "padding-left" : "0 !important",
                "padding-right" : "0 !important",
            },
            "p-3" : {
                "padding" : "0 !important",
            },
            "nav-link" : {
                "font-weight": "400",
                "line-height": "1.6",
                "background-color": "rgba(255, 255, 255, 0) !important",
                "border":" 1px solid rgba(250, 250, 250, 0.2)",
            },
            "nav-link-selected" : {
                "background-color": "rgba(0, 199, 186, 1) !important"
            }
        }
    )

if menu == 'Analisis principal, power bi':
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    import matplotlib.pyplot as plt
    import seaborn as sns

    #Se guardan los dataframes en variables para poder ser usados con más façilidad.
    conectividad= pd.read_csv('streamlit/datasets_clean/conectividad_X_Estado.csv')

    closed_deals = pd.read_csv('streamlit/datasets_clean/closed_deals.csv')
    customers = pd.read_csv('streamlit/datasets_clean/customers.csv')
    geolocation = pd.read_csv('streamlit/datasets_clean/geolocation.csv')
    marketing_qualified_leads = pd.read_csv('streamlit/datasets_clean/marketing_qualified_leads.csv')
    order_items = pd.read_csv('streamlit/datasets_clean/order_items.csv')

    order_payments = pd.read_csv('streamlit/datasets_clean/order_payments.csv')
    order_reviews = pd.read_csv('streamlit/datasets_clean/order_reviews.csv')
    orders = pd.read_csv('streamlit/datasets_clean/orders.csv')
    products = pd.read_csv('streamlit/datasets_clean/products.csv')
    sellers = pd.read_csv('streamlit/datasets_clean/sellers.csv')

    #Organizando los formatos de fecha en el dataframe de orders
    orders['order_estimated_delivery_date'] = pd.to_datetime(orders.order_estimated_delivery_date)
    orders['order_purchase_timestamp'] = pd.to_datetime(orders.order_purchase_timestamp)
    #----------------------------------------------SECCIÓN DE POWER BI--------------------------------------------------
    
    st.markdown("## :bar_chart: Reporte en PowerBI")
    st.markdown("Para ver el reporte, ir al siguiente enlace:")
    st.markdown('[Reporte en PowerBI](https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=871c010f-5e61-4fb1-83ac-98610a7e9110&scope=https%3A%2F%2Fanalysis.windows.net%2Fpowerbi%2Fapi%2F.default%20openid%20profile%20offline_access&redirect_uri=https%3A%2F%2Fapp.powerbi.com%2Fsignin&client-request-id=23b02a41-81f7-4e40-8de9-212f93ffeff9&response_mode=fragment&response_type=code&x-client-SKU=msal.js.browser&x-client-VER=2.25.0&client_info=1&code_challenge=3woiTSJb18U43lzqlGqz99bOucx5_Vj5Hi0AUb_RVwQ&code_challenge_method=S256&nonce=23e22902-513f-417c-83ac-30c3f3098715&state=eyJpZCI6IjdhNjdjNDU1LTY1ZWUtNDlmYi05OGY4LTk0ZjgxNWY2ODA3MiIsIm1ldGEiOnsiaW50ZXJhY3Rpb25UeXBlIjoicmVkaXJlY3QifX0%3D%7C1675138922645.5%3B1675138923446.9&site_id=500453&nux=1)',unsafe_allow_html=True)
    st.markdown("---")

    #----------------------------------------------SECCIÓN DE VENTAS----------------------------------------------------

    #Título de la sección
    st.markdown(f"## :heavy_dollar_sign: Análisis de Ventas")

    #--------------Selección de fechas--------------
    col1, col2 = st.columns(2)
    minim = orders[orders['order_status']=='delivered']['order_purchase_timestamp'].min()
    maxim = orders[orders['order_status']=='delivered']['order_purchase_timestamp'].max()
    start_date = col1.date_input('fecha de inicio', minim)
    end_date = col2.date_input('fecha final', maxim)  
    
    if start_date < end_date:
        st.success('Fecha de inicio: `%s`\n\nFecha final:`%s`' % (start_date, end_date))
    else:
        st.error('Error: la fecha final debe ser despues de la inicial')

    # placeholder
    min_date = np.datetime64(start_date)
    max_date = np.datetime64(end_date)
    orders_2 = orders.copy(deep=True)
    orders_2 = orders_2[(orders_2['order_purchase_timestamp']>=min_date) & (orders_2['order_purchase_timestamp']<=max_date)]
    orders_2['ventas'] = 1
    orders_2 = orders_2.set_index(pd.DatetimeIndex(orders_2['order_purchase_timestamp'])).drop("order_purchase_timestamp",axis=1)
    data_quarter = orders_2[orders_2['order_status']=='delivered']
    data_quarter = data_quarter.resample('Q').sum()

    #--------------Métricas y KPI's--------------
    with st.form('input'):        #Selección de año y trimestre
        st.markdown("Selecciona el año y el trimestre que desees visualizar")
        selected_year = st.selectbox('Selecciona el año:', options = [2018,2017,2016])
        selected_quarter = st.selectbox('Selecciona el trimestre:', options = [1,2,3,4])

        submit_button = st.form_submit_button(label='Confirmar')
    
    if selected_quarter < 4 and selected_year==2016:
        variacion = "sin dato"
    else:
        sales_trim_actual = data_quarter[(data_quarter.index.quarter==selected_quarter) & (data_quarter.index.year==selected_year)].values[0][0]
    
        if selected_quarter == 1:
            selected_quarter_anterior = 4
            selected_year_anterior = selected_year-1 
        else:
            selected_quarter_anterior = selected_quarter-1
            selected_year_anterior = selected_year
    
        sales_trim_pasado = data_quarter[(data_quarter.index.quarter==selected_quarter_anterior) & (data_quarter.index.year==selected_year_anterior)].values[0][0]
        
        variacion = round((sales_trim_actual/sales_trim_pasado-1)*100,2)
    porcentaje_marketing = closed_deals.shape[0]/marketing_qualified_leads.shape[0]
    col1, col2 = st.columns(2)
    col1.metric(label="Variación Porcentual de Ventas", value=variacion)
    col2.metric(label="Porcentaje de Marketing", value=f'{porcentaje_marketing*100}%')

    #--------------Porcentaje de Capatación por Marketing--------------
    st.markdown("### Porcentaje de captación de vendedores por marketing")
    df_temp = pd.DataFrame(marketing_qualified_leads['origin'].value_counts())
    st.table(df_temp)

    #--------------Gráfico de barras--------------
    
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    payment_type = order_payments['payment_type'].unique().tolist()
    counts = list(order_payments['payment_type'].value_counts())

    pastel = sns.color_palette('pastel')
    husl = sns.color_palette('husl')

    plt.rcdefaults()
    fig, ax = plt.subplots()

    # Example data
    sns.barplot(x=payment_type,y=counts,ecolor=[pastel[0],pastel[1],husl[4],pastel[9]])
    st.pyplot(fig)
    #----------------------------------------------SECCIÓN DE CLIENTES--------------------------------------------------

    st.markdown("## :male-office-worker: Análisis de clientes")
    #Organizando los formatos de fecha en el dataframe de orders
    porcentaje_cancelacion = round(orders[orders['order_status']!='delivered'].shape[0]/(orders.shape[0]) *100,2)

    #--------------Métricasy KPI's--------------
    col1, col2 = st.columns(2)
    col1.metric(label="Porcentaje Cancelación de órdenes", value=f'{porcentaje_cancelacion}%')
    col2.metric(label="Variación Trimestral de Ventas completadas", value=100-porcentaje_cancelacion)

    #--------------Gráfico lineal--------------
    st.markdown("### Ventas realizadas mes a mes")
    data_delivered_month = orders_2[orders_2['order_status']=='delivered']
    data_delivered_month =  data_delivered_month.resample('M').sum()
    st.line_chart(data_delivered_month)

    #--------------Gráfico lineal: Cancelaciones por mes--------------
    st.markdown("### Ventas canceladas mes a mes")
    data_canceled_month = orders_2[orders_2['order_status'] =='canceled']
    data_canceled_month =  data_canceled_month.resample('M').sum()
    st.line_chart(data_canceled_month)

    #--------------Top de mejores clientes--------------
    st.markdown("### Top mejores clientes")
    df_temp = pd.DataFrame(customers['customer_unique_id'].value_counts())
    df_temp=df_temp.reset_index()
    df_temp.rename(columns={'index':'customer_unique_ID','customer_unique_id': 'Cantidad de compras'}, inplace=True)
    number = st.number_input('Indique la cantidad de clientes que desea visualizar', min_value = 1)
    st.table(df_temp.head(number))

    st.markdown("---")

    #--------------------------------------SECCIÓN MAPAS CLIENTES-COMPRADORES-----------------------------------------

    st.markdown("## :currency_exchange: Distancia entre clientes y vendedores")
    #Elegimos los dataframes que queremos trabajar con las columnas renombradas igual para poder hacer el merge 
    df_sellers = sellers.rename(columns={'seller_zip_code_prefix':'zip_code_prefix'})
    df_geo = geolocation.rename(columns={'geolocation_zip_code_prefix':'zip_code_prefix'})
    df_geo = df_geo[['zip_code_prefix','geolocation_lat','geolocation_lng']]
    df_customers = customers.rename(columns={'customer_zip_code_prefix':'zip_code_prefix'})

    #Merge (JOIN) de los dataframes
    df_sellers_geo = pd.merge(df_sellers,df_geo, on='zip_code_prefix')
    df_customers_geo = pd.merge(df_customers,df_geo, on='zip_code_prefix')

    #Creación de la métrica
    demora_days = orders[orders['order_status']=='delivered']
    demora_days['order_delivered_customer_date'] = pd.to_datetime(demora_days.order_delivered_customer_date)
    
    demora_days = demora_days[['order_purchase_timestamp','order_delivered_customer_date']]
    demora_days['demora'] = (demora_days['order_delivered_customer_date']-demora_days['order_purchase_timestamp']).dt.days
    demora = demora_days['demora'].mean()
    col1, col2, col3 = st.columns(3)
    col2.metric(label="Promedio de demora en días", value=round(demora,0))

    # Creación de los mapas
    col1, col2 = st.columns(2) #Se crean dos columnas donde van los mapas
    col1.markdown("### Distribución geográfica de vendedores")
    map_data = pd.DataFrame(
        np.array([df_sellers_geo['geolocation_lat'].tolist(),df_sellers_geo['geolocation_lng'].tolist()]).transpose(),
        columns=['lat', 'lon'])
    col1.map(map_data)
    col2.markdown("### Distribución geográfica de compradores")
    map_data = pd.DataFrame(
        np.array([df_customers_geo['geolocation_lat'].tolist(),df_customers_geo['geolocation_lng'].tolist()]).transpose(),
        columns=['lat', 'lon'])
    col2.map(map_data)

    st.markdown("---")
    #----------------------------------------------SECCIÓN DE RESEÑAS--------------------------------------------------
    #Título de la sección
    st.markdown(f"## :scroll: Análisis de Reseñas")

    #Creación de la relación de las tablas necesarias para encontrar la información correspondiente
    df = pd.merge(customers,pd.merge(order_reviews,orders[orders['order_status']=='delivered'], on='order_id'), on = 'customer_id')
 
    option = st.selectbox('Selecciona el estado que desee visualizar', (df['customer_state'].unique()))

    #Conteo de reviews para cada caso: positivos, negativos y neutros
    negativo = df[df["review_score"]<3][df["customer_state"]==option].shape[0]
    neutro = df[(df["review_score"]==3)][df["customer_state"]==option].shape[0]
    positivo = df[(df["review_score"]>3)][df["customer_state"]==option].shape[0]

    #Creación de las métricas
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Score negativo",value=negativo)
    col2.metric(label="Score neutro", value=neutro)
    col3.metric(label="Score positivo", value=positivo)

    score_promedio = round(df[df['customer_state']== option]['review_score'].mean(),2)
    col1, col2, col3 = st.columns(3)
    col1.markdown(f'### El score promedio del estado {option}:')
    col2.markdown(f'## {score_promedio}/5')
    if score_promedio <=1.44:
        col3.markdown("## :star:")
    elif score_promedio <=2.44:
        col3.markdown("## :star: :star:")
    elif score_promedio <=3.44:
        col3.markdown("## :star: :star: :star:")
    elif score_promedio <=4.44:
        col3.markdown("## :star: :star: :star: :star:")
    elif score_promedio > 4.44:
        col3.markdown("## :star: :star: :star: :star:")

    st.markdown("## Comentarios")
    st.table(df[['review_score', 'review_comment_message']][(df['customer_state']==option) & (df['review_comment_message'] != 'no comment')].sort_values('review_score').head(15))

if menu == 'Machine learning: sistema de recomendaciones':
        
    from sklearn.neighbors import NearestNeighbors
    from sklearn.preprocessing import LabelEncoder
    from scipy.sparse import csr_matrix
    le = LabelEncoder()

    df_show =  pd.read_csv('streamlit/datasets_streamlit/df_show.csv')
    df =  pd.read_csv('streamlit/datasets_streamlit/df.csv')
    df_test =  pd.read_csv('streamlit/datasets_streamlit/df_test.csv')

    N = df['customer_le'].unique().shape[0]
    M = df['product_le'].unique().shape[0]

    #creo una matriz que contiene todas las opiniones de todos los productos por todos los custemers, a partir
    #de esto entrenare a mi modelo para que analise similitudes entre los vectores
    X = csr_matrix((df["review_score"].values, (df['product_le'].values, df['customer_le'].values)),shape=(M,N))

    KNN = NearestNeighbors(n_neighbors=10,algorithm='brute',metric='cosine')
    KNN.fit(X)
    def find_similar_products(product_id,matrix,k):
        '''
        se le proporciona el id de un producto y te devuelve un listado de productos similares incluyendo el mismo,
        la metrica predeterminada es cosine
        '''
        neighbours_ids= []
        
        product_vector = matrix[product_id]
        if product_vector.size > 0:
            neighbours = KNN.kneighbors(product_vector, return_distance = True)
            for i in range(1,k+1):
                if neighbours[1].item(i) != product_id:
                    if neighbours[0].item(i) < 0.3:
                        neighbours_ids.append(neighbours[1].item(i))
               
            if len(neighbours_ids) > 0:
                return neighbours_ids
        return None

    st.title("Sistema de recomendaciones")
    st.markdown("#### :robot_face: Modelo de Machine Learning")
    st.markdown("##### Catálogo de productos")
    st.dataframe(df_show)
    product_label_encoder = st.number_input("Ingrese el numero del producto",step=1,format="%i")
    if product_label_encoder:
        list_recomended = find_similar_products(product_label_encoder,X,3)
        if type(list_recomended) == list:
            st.markdown("### Productos recomendados:")
            st.dataframe(df_test.loc[df_test['product_le'].isin(list_recomended)])
        else:
            st.markdown("### No hay sugerencias para el producto seleccionado")
