import  pandas   as pd
import  pydeck   as pdk
import streamlit as st
import folium
from   streamlit_folium import st_folium
st.set_page_config(page_title='SP', page_icon='💥', layout='wide', initial_sidebar_state='expanded')
# DATA:
@st.cache_data
def load_data():
    df      = pd.read_csv('https://github.com/kauefs/dsnp/raw/@/datasets/AcidentesSP.csv')
    columns = {
            'Data do Acidente'                :'date',
            'Hora do Acidente'                :'time',
            'Tipo de via'                     :'road',
            'Município'                       :'area',
            'Logradouro'                      :'address',
            'LAT_(GEO)'                       :'lat',
            'LONG_(GEO)'                      :'lon',
            'Tipo de acidente'                :'accident',
            'Tipo do veículo da vítima'       :'vehicle',
            'Tipo de vítima'                  :'victim',
            'Sexo'                            :'gender',
            'Idade da vítima'                 :'age',
            'Faixa etária'                    :'AgeRange',
            'Tempo entre o Acidente e o óbito':'TimeToDie',
            'Outro Veículo Envolvido'         :'AnotherVehicle',
            }
    df = df.rename(columns, axis=1)
    df = df[list(columns.values())]
    df.dropna(subset = ['lat', 'lon'], inplace=True)
    return df
df          = load_data()
df['date']  = pd.to_datetime(df['date'])
accidents   = df['date'].dt.year.value_counts().sort_index()
# SIDE:
st.sidebar.markdown('''
[![GitHub](  https://img.shields.io/badge/-000000?logo=github&logoColor=FFFFFF)](                                 https://github.com/kauefs/)
[![Medium](  https://img.shields.io/badge/-000000?logo=medium&logoColor=FFFFFF)](                                 https://medium.com/@kauefs)
[![LinkedIn](https://img.shields.io/badge/-0077B5?logo=linkedin&logoColor=FFFFFF)](                               https://www.linkedin.com/in/kauefs/)
[![Python](  https://img.shields.io/badge/-3-4584B6?logo=python&logoColor=FFDE57&labelColor=4584B6&color=646464)](https://www.python.org/)
[![License]( https://img.shields.io/github/license/kauefs/StreamLit?style=flat&logo=apache&logoColor=CB2138&label=License&labelColor=6D6E71&color=D22128)](https://www.apache.org/licenses/LICENSE-2.0)
            ''')
st.sidebar.text( '13 December 2023')
st.sidebar.divider(                )
st.sidebar.title('DashBoard'       )
st.sidebar.bar_chart(accidents, height=200,  color='#00BFFF')
st.sidebar.write('Map Options:')
D3          = st.sidebar.empty()
D2          = st.sidebar.empty()
ano         = st.sidebar.slider('Year:',    2007, 2020, 2015)
FilteredDF  = df[(df.date.dt.year == ano)]
st.sidebar.info( ' {} Accidents'.format(FilteredDF.shape[0]))
table       = st.sidebar.empty()
st.sidebar.divider(            )
st.sidebar.markdown('''©2023™ [ƊⱭȾɅViƧi🧿Ƞ](https://datavision.one/)''')
# MAIN:
st.divider(                    )
st.title(     'Accidents in SP')
st.divider(                    )
st.markdown('''
Tens of thousands of Brazilians loose their lives in the country roads every year.
            ''')
st.divider(    )
if   D3.checkbox( '3D', value=True):
     st.subheader('3D MAP')
     st.pydeck_chart(pdk.Deck(initial_view_state=pdk.ViewState(longitude=-47.00,
                                                               latitude =-23.23,
                                                               zoom     =  6.75,
                                                               min_zoom =  None,
                                                               max_zoom =  None,
                                                               pitch    = 50   ,
                                                               bearing  = 50  ),
                                          layers=[pdk.Layer('HexagonLayer'     ,
                                            data           = FilteredDF,
                                            get_position   = '[lon,lat]',
                                            auto_highlight = True,
                                            elevation_scale= 50,
                                            elevation_range=[ 0,2750],
                                            pickable=True,
                                            extruded=True,
                                            coverage=1)],
                                          views=[{'@@type':'MapView', 'controller':True}],
                                          map_style   ='dark',
                                          api_keys    = None ,
                                          width       ='100%',
                                          height      = 500  ,
                                          tooltip     = True ,
                                          description ='Accidents in SP',
                                          effects     = None ,
                                          map_provider='carto',
                                          parameters  = None))
     st.divider(                   )
if   D2.checkbox( '2D', value=False):
     st.subheader('2D MAP')
     SP    =folium.Map(location=[-23.259505,-47.0628577], zoom_start=6.75,
                     tiles='OpenStreetMap',        prefer_canvas=True)
     map   = df.sample(frac=.025, random_state=0)
     map.dropna(subset = ['lat', 'lon'], inplace=True)
     lat   = map['lat'].values
     lon   = map['lon'].values
     veh   = map['vehicle']
     for lat, lon, veh in zip(lat, lon, veh):
          folium.Marker(location=[lat, lon], popup=veh,
                        icon=folium.Icon(color='red', icon='car-burst', prefix='fa')).add_to(SP)
     st_folium(SP)
     st.divider( )
#     SP    =folium.Map(location=[-23.259505,-47.0628577], zoom_start=6.75,  # noqa: E999
#                     tiles='CartoDB Positron',     prefer_canvas=True)
#     map   = df.copy()
#     map.dropna(subset = ['lat', 'lon'], inplace=True)
#     lat   = map['lat'].values
#     lon   = map['lon'].values
#     def dots(point):
#          '''
#          input: series that contains a numeric named latitude and a numeric named
#          longitude this function creates a CircleMarker and adds it to SP
#          '''
#          folium.CircleMarker(location=[point.lat, point.lon], radius=1.5, weight=3).add_to(SP)
#     map.apply(dots, axis = 1)
#     st_folium(SP)
#     st.divider( )
if   table.checkbox('DataFrame', value=True):
     st.subheader(       'DATA')
     st.markdown(f'''➡️ Showing {'**{}** accidents'.format(FilteredDF.shape[0])} in **{ano}**:''')
     st.write(FilteredDF)
     st.divider(        )
st.toast('Accident!', icon='💥')
