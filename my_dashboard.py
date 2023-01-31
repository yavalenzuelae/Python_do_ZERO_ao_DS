import geopandas
import streamlit as st
import pandas    as pd
import numpy     as np
import folium

from streamlit_folium import folium_static
from folium.plugins   import MarkerCluster

import plotly.express as px
from datetime import datetime

st.set_page_config(layout='wide')

@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)
    return data

@st.cache(allow_output_mutation=True)
def get_data_results(path):
    data01 = pd.read_csv(path + 'planilha_01.csv')
    data02 = pd.read_csv(path + 'planilha_02.csv')
    data31 = pd.read_csv(path + 'planilha_3p1.csv')
    data32 = pd.read_csv(path + 'planilha_3p2.csv')
    return data01, data02, data31, data32
    
@st.cache(allow_output_mutation=True)
def get_geofile(url):
    geofile = geopandas.read_file(url)
    return geofile

def set_feature(data):
    # preço por pé quadrado
    data['price_sqft'] = data['price']/data['sqft_lot']
    return data

def overview_data(data):
    f_attributes = st.sidebar.multiselect('Selecionar Atributos de Interesse', data.columns)
    f_zipcode = st.sidebar.multiselect('Selecionar Regiões', data['zipcode'].unique())

    st.title('Características do Portfólio de Imóveis da House Rocket')
    st.subheader('As informações a seguir correspondem aos dados coletados do site: https://www.kaggle.com/datasets/harlfoxem/housesalesprediction.')
    
    if (f_zipcode != []) and (f_attributes != []):
        data = data.loc[data['zipcode'].isin(f_zipcode), f_attributes]
    elif (f_zipcode != []) and (f_attributes == []):
        data = data.loc[data['zipcode'].isin(f_zipcode), :]
    elif (f_zipcode == []) and (f_attributes != []):
        data = data.loc[:, f_attributes]
    else:
        data = data.copy()

    st.header('Visão Geral dos Dados')
    st.caption('A última columa, price_sqft, da tabela abaixo corresponde ao preço por pé quadrado do imóvel. Este atributo é derivado das colunas price (preço) e sqft_lot (área do loteamento).')
    st.dataframe(data.head())
    
    c1, c2 = st.columns((1, 1))
    # ---------------
    # Average metrics
    # ---------------
    # Número total de imóveis
    df1 = data[['id', 'zipcode']].groupby('zipcode').count().reset_index()
    # média do preço
    df2 = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    # média da área da sala de estar
    df3 = data[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
    # media do preço por pé quadrado
    df4 = data[['price_sqft', 'zipcode']].groupby('zipcode').mean().reset_index()
    # -----
    # Merge
    # -----
    m1 = pd.merge(df1, df2, on='zipcode', how='inner')
    m2 = pd.merge(m1, df3, on='zipcode', how='inner')
    df = pd.merge(m2, df4, on='zipcode', how='inner')
    df.columns = ['zipcode', 'total_houses', 'price', 'sqft_living', 'price_sqft']
    c1.header('Tamanhos e Preços Médios por Região')
    c1.dataframe(df, height=800)
    # ---------------------
    # Statistic Descriptive
    # ---------------------
    num_attributes = data.select_dtypes(include=['int64', 'float64'])
    media = pd.DataFrame(num_attributes.apply(np.mean))
    mediana = pd.DataFrame(num_attributes.apply(np.median))
    std = pd.DataFrame(num_attributes.apply(np.std))
    max_ = pd.DataFrame(num_attributes.apply(np.max))
    min_ = pd.DataFrame(num_attributes.apply(np.min))
    # concatenar
    df1 = pd.concat([max_, min_, media, mediana, std], axis=1).reset_index()
    df1.columns = ['attribute', 'max', 'min', 'mean', 'median', 'std']
    c2.header('Análise Descritivo de cada Atributo')
    c2.dataframe(df1, height=800)
    return None

def get_results(data01, data02, data32):   
    st.title('Recomendações para Compra e Venda')
    c1, c2, c3 = st.columns((1, 1, 1))
    c1.header('Imóveis Sugeridos para Compra')
    c1.caption('Se sugerem imóveis baratos (preços abaixo da mediana da região) e em boas condições. Logo, se assume que não precisam de reformas. A última coluna da tabela abaixo, advise, mostra a recomendação para cada imóvel do portfólio. Os imóveis sugeridos equivalem, aproximadamente, ao 18% do portfólio.')
    c1.dataframe(data01, height=600)
    c2.header('Preços Recomendados para as Vendas')
    c2.caption('Imóveis recomendados para compra localizados perto do centro da cidade e/ou com vista para água possuem uma maior valorização. A coluna, price_sale, dá o preço de venda e a coluna, date_sale, a data sugerida para a venda. O percentual de lucro total equivale aproximadamente a 19,4% do investimento.')
    c2.dataframe(data02, height=600)
    c3.header('Recomendações para Compra, Reforma e Venda')
    c3.caption('Se recomendam imóveis baratos e em condições boas ou regulares. Imóveis em condições regulares e/ou antigos, sem porão, ou com área suficiente para ter mais um quarto, são suceptíveis de reforma. Os imóveis sugeridos equivalem ao 49% do portfólio.  O percentual de lucro total equivale a 89% do investimento.')
    c3.dataframe(data32, height=600)
    return None
    
def portfolio_density(data, data01, data31, data32, geofile):
    st.title('Distribuição e Características dos Imóveis nas Regiões')
    c1, c2 = st.columns([2,1.75])    
    c1.header('Localização dos Imóveis')
    c1.caption('Clique no marcador de interesse para obter maiores informações sobre o imóvel. No mapa são mostradas somente 20 localizações. Recarregue a paǵina para visualizar outras localizações (Ctrl + r).')    
    # número de imóveis mostrados no mapa
    df = data.sample(10)
    # merge 
    df1 = df.merge(data31[['id','cond_type','advise']], how='left', on='id')
    # merge
    df2 = df1.merge(data32[['id','price_sale','gain_tot','date_sale']], how='left', on='id')
    # check nan
    df2[['price_sale','gain_tot','date_sale']] = df2[['price_sale','gain_tot','date_sale']].fillna('NA')
    # Base Map - Folium
    density_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()], zoom_start=9)
    
    marker_cluster = MarkerCluster().add_to(density_map)
    for name, row in df2.iterrows():
        if row['advise'] == 'buy':
            folium.Marker([row['lat'], row['long']], popup='ID do Imóvel: {0}. Preço: {1}. Condição: {2}. Sugestão: {3}. Preço de venda: {4}. Margem: {5}. Data para Venda: {6}. Características: área de estar de {7} sqft, {8} quartos, {9} banheiros, ano de construção {10}'.format(row['id'], row['price'], row['cond_type'], row['advise'], row['price_sale'], row['gain_tot'], row['date_sale'], row['sqft_living'], row['bedrooms'], row['bathrooms'], row['yr_built'])).add_to(marker_cluster)
        else:
            folium.Marker([row['lat'], row['long']], popup='ID do Imóvel: {0}. Preço: {1}. Condição: {2}. Sugestão: {3}.'.format(row['id'], row['price'], row['cond_type'], row['advise'])).add_to(marker_cluster)

    with c1:
        folium_static(density_map)

    # Region Price Map
    c2.header('Preços Médios por Região')
    c2.caption('Na escala abaixo as cores mais claras correspondem a preços menores e as mais escuras a preços maiores. Os contornos pretos delimitam as regiões dos imóveis do portfólio.')
    
    df = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    df.columns = ['ZIP', 'PRICE']

    geofile = geofile[geofile['ZIP'].isin(df['ZIP'].tolist())]

    region_price_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()], zoom_start=9)
    
    region_price_map.choropleth(data=df, geo_data=geofile, columns=['ZIP', 'PRICE'], key_on='feature.properties.ZIP',
                                fill_color='YlOrRd', fill_opacity=0.8, line_opacity=0.85, legend_name='Preço médio')

    with c2:
        folium_static(region_price_map)
    return None

def commercial(data):
    st.sidebar.title('Opções dos Atributos Comerciais')
    st.title('Atributos Comerciais')
    # ----------------------
    # Average Price per Year
    # ----------------------
    # filter
    min_year_built = int(data['yr_built'].min())
    max_year_built = int(data['yr_built'].max())
    st.sidebar.subheader('Selecione o Ano de Construção Máximo')
    f_year_built = st.sidebar.slider('Ano de Construção', min_year_built, max_year_built, min_year_built)

    st.header('Preço Médio por Ano de Construção')
    st.caption('Começando desde 1900 e até o Ano de Construção (Máximo) selecionado.')
    # data selection
    df = data.loc[data['yr_built'] < f_year_built]
    df = df[['yr_built', 'price']].groupby('yr_built').mean().reset_index()
    # plot
    fig = px.line(df, x='yr_built', y='price')
    st.plotly_chart(fig, use_container_width=True)
    # ---------------------
    # Average Price per Day
    # ---------------------
    st.header('Preço Médio por dia')
    st.caption('Começando desde 2014-05-02 e até a Data (da Venda) Máxima selecionada.')
    st.sidebar.subheader('Selecione a Data (da Venda) Máxima')

    # get data
    data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')

    # filters
    min_date = datetime.strptime(data['date'].min(), '%Y-%m-%d')
    max_date = datetime.strptime(data['date'].max(), '%Y-%m-%d')

    f_date = st.sidebar.slider('Data', min_date, max_date, min_date)

    # data filtering
    data['date'] = pd.to_datetime(data['date'])
    df = data.loc[data['date'] < f_date]
    df = df[['date', 'price']].groupby('date').mean().reset_index()
    fig = px.line(df, x='date', y='price')
    st.plotly_chart(fig, use_container_width=True)
    # ---------
    # histogram
    # ---------
    st.header('Quantidade de Imóveis por Preço')
    st.caption('Começando desde 75000 e até o Preço Máximo selecionado.')
    st.sidebar.subheader('Selecione o Preço Máximo')

    # filter
    min_price = int(data['price'].min())
    max_price = int(data['price'].max())
    avg_price = int(data['price'].mean())
    # data filtering
    f_price = st.sidebar.slider('Preço', min_price, max_price, avg_price)
    df = data.loc[data['price'] < f_price]
    # data plot
    fig = px.histogram(df, x='price', nbins=50)
    st.plotly_chart(fig, use_container_width=True)
    return None

def attributes_distribution(data):
    st.sidebar.title('Opções dos Atributos dos Imóveis')
    st.title('Atributos dos Imóveis')

    # filter
    f_bedrooms = st.sidebar.selectbox('Número Máximo de Quartos', sorted(set(data['bedrooms'].unique())))
    f_bathrooms = st.sidebar.selectbox('Número Máximo de Banheiros', sorted(set(data['bathrooms'].unique())))
    c1, c2 = st.columns(2)

    # house per bedrooms
    c1.header('Imóveis por Número de Quartos')
    c1.caption('Valores na faixa entre 0 (imóvel SEM quartos) e 33')
    df = data[data['bedrooms'] < f_bedrooms]
    fig = px.histogram(df, x='bedrooms', nbins=19)
    c1.plotly_chart(fig, use_container_width=True)

    # house per bathrooms
    c2.header('Imóveis por Número de Banheiros')
    c2.caption('Valores com casas decimais representam banheiros sem um o mais ítens entre: lavabo, vaso, chuveiro e banheira.')
    df = data[data['bathrooms'] < f_bathrooms]
    fig = px.histogram(df, x='bathrooms', nbins=19)
    c2.plotly_chart(fig, use_container_width=True)

    # filters
    f_floors = st.sidebar.selectbox('Número Máximo de Andares', sorted(set(data['floors'].unique())))
    # Alternative: data['bathrooms'].sort_values().unique()
    f_waterview = st.sidebar.checkbox('Imóveis com Vista para Água')
    c1, c2 = st.columns(2)

    # house per floors
    c1.header('Imóveis por Número de Andares')
    c1.caption('Valores com casas decimais representam andares superiores como sendo uma fração do andar anterior.')
    df = data[data['floors'] < f_floors]
    fig = px.histogram(df, x='floors', nbins=19)
    c1.plotly_chart(fig, use_container_width=True)

    # houses per water view
    c2.header('Imóveis com Atributos Especiais')
    c2.caption('O "0" corresponde a imóveis SEM vista para água e o "1" corresponde a imóveis COM vista para água')
    if f_waterview:
        df = data[data['waterfront'] == 1]
    else:
        df = data.copy()
    fig = px.histogram(df, x='waterfront', nbins=10)
    c2.plotly_chart(fig, use_container_width=True)
    return None

if __name__ == '__main__':
    # ETL
    # ---------------
    # data extraction
    # ---------------
    path = 'data/kc_house_data.csv'
    path_res = 'results/'
    url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
    data = get_data(path)
    data01, data02, data31, data32 = get_data_results(path_res)
    geofile = get_geofile(url)
    # --------------
    # transformation
    # --------------
    data = set_feature(data)
    overview_data(data)
    get_results(data01, data02, data32)
    portfolio_density(data, data01, data31, data32, geofile)
    commercial(data)
    attributes_distribution(data)
    # -------
    # loading
    # -------
    # OBS: como não estamos salvando nada em API ou Banco de dados não preenchemos nada aqui
