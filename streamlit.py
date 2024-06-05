import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import json
import os
import sqlite3
from sqlalchemy import create_engine
import requests
from PIL import Image

#db connection
conn = sqlite3.connect('phonepe.db')

# Create an SQLite engine
engine = create_engine('sqlite:///phonepe.db')

#calling curr dataframes from sqlite
curr = conn.cursor()
#Agg_Trans
curr.execute("select * from Agg_Trans")
conn.commit()
table1 = curr.fetchall()
df1 =pd.DataFrame(table1,columns =["State","Year","Quater","Transacion_type","Transacion_count","Transacion_amount"])

#Agg_User
curr.execute("select * from Agg_User")
conn.commit()
table2 = curr.fetchall()
df2 =pd.DataFrame(table2,columns =["State","Year","Quater","Brands","Transacion_count","Percentage"])

#map_Trans
curr.execute("select * from map_Trans")
conn.commit()
table3 = curr.fetchall()
df3 =pd.DataFrame(table3,columns =["State","Year","Quater","Districts","Transacion_count","Transacion_amount"])

#map_User
curr.execute("select * from map_User")
conn.commit()
table4 = curr.fetchall()
df4 =pd.DataFrame(table4,columns =["State","Year","Quater","Districts","RegisteredUsers","AppOpens"])

#top_Trans
curr.execute("select * from top_Trans")
conn.commit()
table5 = curr.fetchall()
df5 =pd.DataFrame(table5,columns =["State","Year","Quater","Pincodes","Transacion_count","Transacion_amount"])

#top_User
curr.execute("select * from top_User")
conn.commit()
table6 = curr.fetchall()
df6 =pd.DataFrame(table6,columns =["State","Year","Quater","Pincodes","RegisteredUsers"])


# year func agg trans plot
def tac_Y(year):
    curr = conn.cursor()
    curr.execute(f"select Year,State,sum(Transacion_count),sum(Transacion_amount) from  Agg_Trans where Year ={year} group by State;")

    table1 = curr.fetchall()
    tgrp =pd.DataFrame(table1,columns =["Year","State","Transacion_count","Transacion_amount"])
    #tgrp
    
    col1,col2 = st.columns(2)
    with col1:
      fig_count =px.bar(tgrp,x='State',y='Transacion_count',color_discrete_sequence=px.colors.sequential.Bluered_r,height =650,width =600).update_layout(
                  title = dict(text=f"{year} Transaction Count",font=dict(size=20, color='black'),x=0.5,y=1.0),
              xaxis_title=dict(text ='States',font=dict(size=10, color='black')),
              yaxis_title=dict(text ='Transaction Count',font=dict(size=10, color='black')),
              plot_bgcolor='rgba(0, 0, 0, 0)',
              paper_bgcolor='rgba(0, 0, 0, 0)')
      st.plotly_chart(fig_count)
    with col2:
      fig_amt =px.bar(tgrp,x='State',y='Transacion_amount',color_discrete_sequence=px.colors.sequential.Bluered_r,height =650,width =600).update_layout(
                  title = dict(text=f"{year} Transaction Amount",font=dict(size=20, color='black'),x=0.5,y=1.0),
              xaxis_title=dict(text ='States',font=dict(size=10, color='black')),
              yaxis_title=dict(text ='Transaction Amount',font=dict(size=10, color='black')),plot_bgcolor='rgba(0, 0, 0, 0)',
              paper_bgcolor='rgba(0, 0, 0, 0)')
      st.plotly_chart(fig_amt)
      
    #india map
    
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response =requests.get(url)
    data1 =json.loads(response.content)
    states_names =[]
    for feature in data1['features']:
        states_names.append(feature["properties"]["ST_NM"]) 
        states_names.sort() 
        
    fig_india = px.choropleth(tgrp,geojson = data1, locations ="State",
                featureidkey = "properties.ST_NM",
                color ="Transacion_count",
                color_continuous_scale ="twilight",
                range_color =(tgrp["Transacion_count"].min(),tgrp["Transacion_count"].max(),
                              (tgrp["Transacion_amount"].min(),tgrp["Transacion_amount"].max())),
                 hover_data=["Transacion_amount"], 
                fitbounds ="locations",basemap_visible=False,
                height =650, width =600).update_layout(title = dict(text=f"{year} All Transaction",font=dict(size=20, color='black'),x=0.5,y=0.9),
                  geo=dict(bgcolor= 'rgba(0,0,0,0)'),paper_bgcolor='rgba(0, 0, 0, 0)')
    fig_india.layout.coloraxis.colorbar.title = 'Transaction_Range'            
    st.plotly_chart(fig_india,use_container_width=True)
    
  
#agg trans quater function

def tac_Q(year,quater):
    curr = conn.cursor()
    curr.execute(f"select Quater, State,sum(Transacion_count),sum(Transacion_amount) from  Agg_Trans where Quater ={quater} and Year={year} group by State;")
    table1 = curr.fetchall()
    tgrp =pd.DataFrame(table1,columns =["Quater","State","Transacion_count","Transacion_amount"])
    #tgrp

    col1,col2 = st.columns(2)
    with col1:
      fig_count =px.bar(tgrp,x='State',y='Transacion_count',color_discrete_sequence=px.colors.sequential.Bluered_r,height =650, width =600).update_layout(
                  title = dict(text=f"{year}'s {quater} Quater's Transaction Count",font=dict(size=20, color='black'),x=0.2,y=1.0),
              xaxis_title=dict(text ='States'), yaxis_title=dict(text ='Transaction Count'),
              plot_bgcolor='rgba(0, 0, 0, 0)',
              paper_bgcolor='rgba(0, 0, 0, 0)')
      st.plotly_chart(fig_count)
      
    with col2:
      fig_amt =px.bar(tgrp,x='State',y='Transacion_amount',color_discrete_sequence=px.colors.sequential.Bluered_r,height =650, width =600,).update_layout(
                  title = dict(text=f"{year}'s {quater} Quater's Transaction Amount",font=dict(size=20, color='black'),x=0.2,y=1.0),
              xaxis_title=dict(text ='States'), yaxis_title=dict(text ='Transaction Amount'),
              plot_bgcolor='rgba(0, 0, 0, 0)',
              paper_bgcolor='rgba(0, 0, 0, 0)')
      st.plotly_chart(fig_amt)
    
    #india map
    
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response =requests.get(url)
    data1 =json.loads(response.content)
    states_names =[]
    for feature in data1['features']:
        states_names.append(feature["properties"]["ST_NM"]) 
        states_names.sort() 
        
    fig_india = px.choropleth(tgrp,geojson = data1, locations ="State",
                featureidkey = "properties.ST_NM",
                color ="Transacion_count",
                color_continuous_scale ="twilight",
                range_color =(tgrp["Transacion_count"].min(),tgrp["Transacion_count"].max(),
                              (tgrp["Transacion_amount"].min(),tgrp["Transacion_amount"].max())),
                 hover_data=["Transacion_amount"], 
                fitbounds ="locations",basemap_visible=False,
                height =650, width =600).update_layout(title = dict(text=f"{year}'s {quater}Quater's All Transaction",font=dict(size=20, color='black'),x=0.5,y=0.9),
                                                       geo=dict(bgcolor= 'rgba(0,0,0,0)'),paper_bgcolor='rgba(0, 0, 0, 0)')
    fig_india.layout.coloraxis.colorbar.title = 'Transaction_Range'            
    st.plotly_chart(fig_india,use_container_width=True)    
    
    #agg trans types
    
def tac_T(year,states):
    curr = conn.cursor()
    curr.execute(f"select Year,State,Transacion_type,sum(Transacion_count),sum(Transacion_amount) from  Agg_Trans where State ='{states}' and Year = {year} group by Transacion_type;")

    table1 = curr.fetchall()
    tgrp =pd.DataFrame(table1,columns =["Year","State","Transacion_type","Transacion_count","Transacion_amount"])
  #tgrp

    col1,col2 = st.columns(2)
    with col1:
        fig_pie =px.pie(tgrp ,names='Transacion_type',values='Transacion_amount',hole =0.5,height =650, width =600).update_layout(
                title = dict(text=f"{states} Transaction Amount",font=dict(size=20, color='black'),x=0.2,y=1.0),
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)')
        st.plotly_chart(fig_pie)
    with col2:
      st.header(":blue[_CATAGORY_]")
      curr = conn.cursor()
      curr.execute(f"select Transacion_type,sum(Transacion_count),sum(Transacion_amount) from  Agg_Trans where State ='{states}'  group by Transacion_type;")
      table1 = curr.fetchall()
      cat =pd.DataFrame(table1,columns =["Transacion_type","Transacion_count","Transacion_amount"])
      st.dataframe(cat.style.background_gradient(cmap='Blues'),use_container_width=True, hide_index=True)
 # agg User year plot     
def ubc_Y(year):
    curr = conn.cursor()
    curr.execute(f"select Year,Brands,sum(Transacion_count),sum(Percentage) from  Agg_User where Year = {year} group by Brands;")

    table1 = curr.fetchall()
    ugrp =pd.DataFrame(table1,columns =["Year","Brands","Transacion_count","Percentage"])
    #ugrp
 
    fig_brand =px.bar(ugrp,x="Brands",y ="Transacion_count",color_discrete_sequence=px.colors.sequential.Turbo).update_layout(
                title = dict(text=f"{year}'s Brands and Transaction Count",font=dict(size=20, color='black'),x=0.2,y=0.9),
            xaxis_title=dict(text ='Brands'), yaxis_title=dict(text ='Transaction Count'), plot_bgcolor='rgba(0, 0, 0, 0)',
               paper_bgcolor='rgba(0, 0, 0, 0)')
    st.plotly_chart(fig_brand,use_container_width=True) 
    
# agg User Quarter func  
def ubc_Q(year,quater):
    curr = conn.cursor()
    curr.execute(f"select Year,Quater,Brands,sum(Transacion_count),sum(Percentage) from  Agg_User where Quater ={quater} and Year={year} group by Brands;")
    table1 = curr.fetchall()
    ugrp =pd.DataFrame(table1,columns =["Year","Quater","Brands","Transacion_count","Percentage"])
  #ugrp

    fig_brand =px.bar(ugrp,x="Brands",y ="Transacion_count",color_discrete_sequence=px.colors.sequential.Inferno).update_layout(
                title = dict(text=f"{year}'s {quater} Quarter's Brands and Transaction Count",font=dict(size=20, color='black'),x=0.2,y=0.9),
            xaxis_title=dict(text ='Brands'), yaxis_title=dict(text ='Transaction Count'), plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)')
    st.plotly_chart(fig_brand,use_container_width=True)
 # agg User states   
def ubc_S(years):
    curr = conn.cursor()
    curr.execute(f"select Year,State,Brands,sum(Transacion_count),sum(Percentage) from  Agg_User where Year={years} group by Brands;")
    table1 = curr.fetchall()
    ugrp =pd.DataFrame(table1,columns =["Year","State","Brands","Transacion_count","Percentage"])
    #ugrp
    fig = px.bar(ugrp, x="Brands", y="Transacion_count",hover_name ="Brands",color='Percentage',
                                color_continuous_scale='viridis',
                        animation_frame="State", barmode='group').update_layout(
                        title = dict(text=f"{years}'s Brand's Percentage Range",font=dict(size=20, color='black'),x=0.2,y=0.9),
                        xaxis_title=dict(text ='Brands'), yaxis_title=dict(text ='Transaction Count'),transition={'duration': 3000000},
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      paper_bgcolor='rgba(0, 0, 0, 0)')
    st.plotly_chart(fig,use_container_width=True)  

#map trans year
def map_Y(year):
    curr = conn.cursor()
    curr.execute(f"select Year,State,sum(Transacion_count),sum(Transacion_amount) from  map_Trans where Year ={year} group by State;")

    table1 = curr.fetchall()
    tgrp =pd.DataFrame(table1,columns =["Year","State","Transacion_count","Transacion_amount"])
    #tgrp
    col1,col2 = st.columns(2)
    with col1:
      fig_count =px.bar(tgrp,x='State',y='Transacion_count',color_discrete_sequence=px.colors.sequential.Bluered_r,height =650,width =600).update_layout(
                  title = dict(text=f"{year} Transaction Count",font=dict(size=20, color='black'),x=0.5,y=1.0),
              xaxis_title=dict(text ='States',font=dict(size=10, color='black')),
              yaxis_title=dict(text ='Transaction Count',font=dict(size=10, color='black')),
              plot_bgcolor='rgba(0, 0, 0, 0)',
              paper_bgcolor='rgba(0, 0, 0, 0)')
      st.plotly_chart(fig_count)
    with col2:
      fig_amt =px.bar(tgrp,x='State',y='Transacion_amount',color_discrete_sequence=px.colors.sequential.Bluered_r,height =650,width =600).update_layout(
                  title = dict(text=f"{year} Transaction Amount",font=dict(size=20, color='black'),x=0.5,y=1.0),
              xaxis_title=dict(text ='States',font=dict(size=10, color='black')),
              yaxis_title=dict(text ='Transaction Amount',font=dict(size=10, color='black')),plot_bgcolor='rgba(0, 0, 0, 0)',
              paper_bgcolor='rgba(0, 0, 0, 0)')
      st.plotly_chart(fig_amt)
  
 #india map
    
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response =requests.get(url)
    data1 =json.loads(response.content)
    states_names =[]
    for feature in data1['features']:
        states_names.append(feature["properties"]["ST_NM"]) 
        states_names.sort() 
        
    fig_india = px.choropleth(tgrp,geojson = data1, locations ="State",
                featureidkey = "properties.ST_NM",
                color ="Transacion_count",
                color_continuous_scale ="twilight",
                range_color =(tgrp["Transacion_count"].min(),tgrp["Transacion_count"].max(),
                              (tgrp["Transacion_amount"].min(),tgrp["Transacion_amount"].max())),
                 hover_data=["Transacion_amount"], 
                fitbounds ="locations",basemap_visible=False,
                height =650, width =600).update_layout(title = dict(text=f"{year} All Transaction",font=dict(size=20, color='black'),x=0.5,y=0.9),
                  geo=dict(bgcolor= 'rgba(0,0,0,0)'),paper_bgcolor='rgba(0, 0, 0, 0)')
    fig_india.layout.coloraxis.colorbar.title = 'Transaction_Range'            
    st.plotly_chart(fig_india,use_container_width=True)

# MAP TRANS QUATER    
def map_Q(year,quater):
    curr = conn.cursor()
    curr.execute(f"select Quater, State,sum(Transacion_count),sum(Transacion_amount) from  map_Trans where Quater ={quater} and Year={year} group by State;")
    table1 = curr.fetchall()
    tgrp =pd.DataFrame(table1,columns =["Quater","State","Transacion_count","Transacion_amount"])
    #tgrp

    col1,col2 = st.columns(2)
    with col1:
      fig_count =px.bar(tgrp,x='State',y='Transacion_count',color_discrete_sequence=px.colors.sequential.Bluered_r,height =650, width =600).update_layout(
                  title = dict(text=f"{year}'s {quater} Quater's Transaction Count",font=dict(size=20, color='black'),x=0.2,y=1.0),
              xaxis_title=dict(text ='States'), yaxis_title=dict(text ='Transaction Count'),
              plot_bgcolor='rgba(0, 0, 0, 0)',
              paper_bgcolor='rgba(0, 0, 0, 0)')
      st.plotly_chart(fig_count)
      
    with col2:
      fig_amt =px.bar(tgrp,x='State',y='Transacion_amount',color_discrete_sequence=px.colors.sequential.Bluered_r,height =650, width =600,).update_layout(
                  title = dict(text=f"{year}'s {quater} Quater's Transaction Amount",font=dict(size=20, color='black'),x=0.2,y=1.0),
              xaxis_title=dict(text ='States'), yaxis_title=dict(text ='Transaction Amount'),
              plot_bgcolor='rgba(0, 0, 0, 0)',
              paper_bgcolor='rgba(0, 0, 0, 0)')
      st.plotly_chart(fig_amt)
      
 #india map
    
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response =requests.get(url)
    data1 =json.loads(response.content)
    states_names =[]
    for feature in data1['features']:
        states_names.append(feature["properties"]["ST_NM"]) 
        states_names.sort() 
        
    fig_india = px.choropleth(tgrp,geojson = data1, locations ="State",
                featureidkey = "properties.ST_NM",
                color ="Transacion_count",
                color_continuous_scale ="twilight",
                range_color =(tgrp["Transacion_count"].min(),tgrp["Transacion_count"].max(),
                              (tgrp["Transacion_amount"].min(),tgrp["Transacion_amount"].max())),
                hover_data=["Transacion_amount"], 
                fitbounds ="locations",basemap_visible=False,
                height =650, width =600).update_layout(title = dict(text=f"{year}'s {quater}Quater's All Transaction",font=dict(size=20, color='black'),x=0.5,y=0.9),
                                                      geo=dict(bgcolor= 'rgba(0,0,0,0)'),paper_bgcolor='rgba(0, 0, 0, 0)')
    fig_india.layout.coloraxis.colorbar.title = 'Transaction_Range'            
    st.plotly_chart(fig_india,use_container_width=True) 
        
#map trans func for districts
def map_D(years,states):
    curr = conn.cursor()
    curr.execute(f"select State,Districts,sum(Transacion_count),sum(Transacion_amount) from  map_Trans where Year = {years} and State ='{states}'  group by Districts;")

    table1 = curr.fetchall()
    mgrp =pd.DataFrame(table1,columns =["State","Districts","Transacion_count","Transacion_amount"])
    #mgrp
    fig = px.bar(mgrp, y='Districts',x='Transacion_count',hover_name ="State",color='Transacion_amount',
                                color_continuous_scale='viridis'
                         ).update_layout(
                        title = dict(text=f"{years} {states} District wise Transaction",font=dict(size=20, color='black'),x=0.2,y=0.9),
                       transition={'duration': 3000000},yaxis_title=dict(text ='Districts',font=dict(color='black')),
                       xaxis_title=dict(text ='Transaction count',font=dict(color='black')),plot_bgcolor='rgba(0, 0, 0, 0)',
                       paper_bgcolor='rgba(0, 0, 0, 0)')
    st.plotly_chart(fig,use_container_width=True)
    
   #map User func
def mu_Y(year):
    curr = conn.cursor()
    curr.execute(f"select Year,State,sum(RegisteredUsers),sum(AppOpens) from  map_User where Year ={year} group by State;")

    table1 = curr.fetchall()
    mgrp =pd.DataFrame(table1,columns =["Year","State","RegisteredUsers","AppOpens"])
    #mgrp
    fig_line =px.line(mgrp, x='State',y="RegisteredUsers",color_discrete_sequence=px.colors.sequential.Magenta_r,markers="*",height = 800).update_layout(
                title = dict(text=f"{year} Registered Users",font=dict(size=20, color='black'),x=0.5,y=1.0),
            xaxis_title=dict(text ='STATES',font=dict(color='black')), yaxis_title=dict(text ='Registered Users',font=dict(color='black')),plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)').update_yaxes(tickfont=dict(color='black',
                                                            size=18)).update_xaxes(tickfont=dict(color='black', size=15))
    st.plotly_chart(fig_line,use_container_width=True)
# map user quater       
def mu_Q(year):  
    curr = conn.cursor()
    curr.execute(f"select Year,Quater,State,RegisteredUsers,AppOpens from  map_User where Year = {year};")

    table1 = curr.fetchall()
    mgrp =pd.DataFrame(table1,columns =["Year","Quater","State","RegisteredUsers","AppOpens"])
    #mgrp
    fig_line =px.line(mgrp, x='State',y="RegisteredUsers",color_discrete_sequence=px.colors.sequential.Reds_r,
                   height = 800, animation_frame="Quater").update_layout(sliders=dict(yanchor = 'top',x=0.1,y=1.0),
               title = dict(text=f"{year} Registered Users",font=dict(size=20, color='black'),x=0.5,y=0.9),
            xaxis_title=dict(text ='States',font=dict(color='black')), yaxis_title=dict(text ='Registered Users',font=dict(color='black')),
            plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0, 0, 0, 0)').update_yaxes(tickfont=dict(color='black',
                                                            size=18)).update_xaxes(tickfont=dict(color='black', size=15))
    st.plotly_chart(fig_line,use_container_width=True)
    
# map user appopens
def app(year):
    curr = conn.cursor()
    curr.execute(f"select Year,State,sum(RegisteredUsers),sum(AppOpens) from  map_User where Year ={year} group by State;")

    table1 = curr.fetchall()
    mgrp =pd.DataFrame(table1,columns =["Year","State","RegisteredUsers","AppOpens"])
    #mgrp
    data = {'Latitude': [11.6234, 16.5062, 27.0844, 26.1445, 25.5941, 30.7333, 21.2514,
                 20.3974, 28.7041, 15.4909, 23.2156, 30.7333, 31.1048, 34.0837,
                 23.3441, 12.9716, 8.5241, 34.1526, 10.5667, 23.2599, 19.0760,
                 24.8170, 25.5788, 23.1645, 25.6751, 20.2961, 11.9416, 30.7333,
                 26.9124, 27.3314, 13.0827, 17.3850, 23.8315, 26.8467, 30.3165,
                 22.5726],
            'Longitude': [92.7265, 80.6480, 93.6053, 91.7362, 85.1376, 76.7794, 81.6296,
                  72.8328, 77.1025, 73.8278, 72.6369, 76.7794, 77.1734, 74.7973,
                  85.3096, 77.5946, 76.9366, 77.5771, 72.6369, 77.4126, 72.8777,
                  93.9368, 91.8933, 92.9376, 94.1086, 85.8245, 79.8083, 76.7794,
                  75.7873, 88.6138, 80.2707, 78.4867, 91.2868, 80.9462, 78.0322,
                  88.3639]}
    loc = pd.DataFrame(data)
    new= loc.join(mgrp)

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response =requests.get(url)
    data1 =json.loads(response.content)
    states_names =[]
    for feature in data1['features']:
        states_names.append(feature["properties"]["ST_NM"]) 
        states_names.sort() 
    fig_india = px.choropleth(mgrp,geojson = data1, locations ="State",
                featureidkey = "properties.ST_NM",
                color_discrete_sequence=px.colors.sequential.haline_r, 
                fitbounds ="locations",basemap_visible=False,
                height =650, width =600).update_layout(title = dict(text=f"{year}'s Appopens by User's",font=dict(size=20, color='black'),x=0.5,y=0.9))
            
    # # Add scatter plot
    fig = px.scatter_geo(new, lat="Latitude", lon="Longitude",color="AppOpens",fitbounds ="locations",basemap_visible=False,
                        hover_data=["State"],
                    color_continuous_scale="Rainbow", size_max=15)
    
    fig_india.add_trace(fig.data[0])
    fig_india.layout.coloraxis.colorbar.title = 'Appopens_Range'
    fig_india.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)',geo=dict(bgcolor= 'rgba(0,0,0,0)'))   
    st.plotly_chart(fig_india,use_container_width=True)
## TOP TRANS YEAR
def top_Y(year):
    curr = conn.cursor()
    curr.execute(f"select Year,State,sum(Transacion_count),sum(Transacion_amount) from  top_Trans where Year ={year} group by State;")

    table1 = curr.fetchall()
    tgrp =pd.DataFrame(table1,columns =["Year","State","Transacion_count","Transacion_amount"])
    #tgrp

    col1,col2 = st.columns(2)
    with col1:
      fig_count =px.bar(tgrp,x='State',y='Transacion_count',color_discrete_sequence=px.colors.sequential.Bluered_r,height =650,width =600).update_layout(
                  title = dict(text=f"{year} Transaction Count",font=dict(size=20, color='black'),x=0.5,y=1.0),
              xaxis_title=dict(text ='States',font=dict(size=10, color='black')),
              yaxis_title=dict(text ='Transaction Count',font=dict(size=10, color='black')),
              plot_bgcolor='rgba(0, 0, 0, 0)',
              paper_bgcolor='rgba(0, 0, 0, 0)')
      st.plotly_chart(fig_count)
    with col2:
      fig_amt =px.bar(tgrp,x='State',y='Transacion_amount',color_discrete_sequence=px.colors.sequential.Bluered_r,height =650,width =600).update_layout(
                  title = dict(text=f"{year} Transaction Amount",font=dict(size=20, color='black'),x=0.5,y=1.0),
              xaxis_title=dict(text ='States',font=dict(size=10, color='black')),
              yaxis_title=dict(text ='Transaction Amount',font=dict(size=10, color='black')),plot_bgcolor='rgba(0, 0, 0, 0)',
              paper_bgcolor='rgba(0, 0, 0, 0)')
      st.plotly_chart(fig_amt)
      
    #india map
    
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response =requests.get(url)
    data1 =json.loads(response.content)
    states_names =[]
    for feature in data1['features']:
        states_names.append(feature["properties"]["ST_NM"]) 
        states_names.sort() 
        
    fig_india = px.choropleth(tgrp,geojson = data1, locations ="State",
                featureidkey = "properties.ST_NM",
                color ="Transacion_count",
                color_continuous_scale ="twilight",
                range_color =(tgrp["Transacion_count"].min(),tgrp["Transacion_count"].max(),
                              (tgrp["Transacion_amount"].min(),tgrp["Transacion_amount"].max())),
                 hover_data=["Transacion_amount"], 
                fitbounds ="locations",basemap_visible=False,
                height =650, width =600).update_layout(title = dict(text=f"{year} All Transaction",font=dict(size=20, color='black'),x=0.5,y=0.9),
                  geo=dict(bgcolor= 'rgba(0,0,0,0)'),paper_bgcolor='rgba(0, 0, 0, 0)')
    fig_india.layout.coloraxis.colorbar.title = 'Transaction_Range'            
    st.plotly_chart(fig_india,use_container_width=True)
# map trans quater
def top_Q(year,quater):
    curr = conn.cursor()
    curr.execute(f"select Quater, State,sum(Transacion_count),sum(Transacion_amount) from  top_Trans where Quater ={quater} and Year={year} group by State;")
    table1 = curr.fetchall()
    tgrp =pd.DataFrame(table1,columns =["Quater","State","Transacion_count","Transacion_amount"])    
    #tgrp

    col1,col2 = st.columns(2)
    with col1:
      fig_count =px.bar(tgrp,x='State',y='Transacion_count',color_discrete_sequence=px.colors.sequential.Bluered_r,height =650, width =600).update_layout(
                  title = dict(text=f"{year}'s {quater} Quater's Transaction Count",font=dict(size=20, color='black'),x=0.2,y=1.0),
              xaxis_title=dict(text ='States'), yaxis_title=dict(text ='Transaction Count'),
              plot_bgcolor='rgba(0, 0, 0, 0)',
              paper_bgcolor='rgba(0, 0, 0, 0)')
      st.plotly_chart(fig_count)
      
    with col2:
      fig_amt =px.bar(tgrp,x='State',y='Transacion_amount',color_discrete_sequence=px.colors.sequential.Bluered_r,height =650, width =600,).update_layout(
                  title = dict(text=f"{year}'s {quater} Quater's Transaction Amount",font=dict(size=20, color='black'),x=0.2,y=1.0),
              xaxis_title=dict(text ='States'), yaxis_title=dict(text ='Transaction Amount'),
              plot_bgcolor='rgba(0, 0, 0, 0)',
              paper_bgcolor='rgba(0, 0, 0, 0)')
      st.plotly_chart(fig_amt)
#india map
    
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response =requests.get(url)
    data1 =json.loads(response.content)
    states_names =[]
    for feature in data1['features']:
        states_names.append(feature["properties"]["ST_NM"]) 
        states_names.sort() 
        
    fig_india = px.choropleth(tgrp,geojson = data1, locations ="State",
                featureidkey = "properties.ST_NM",
                color ="Transacion_count",
                color_continuous_scale ="twilight",
                range_color =(tgrp["Transacion_count"].min(),tgrp["Transacion_count"].max(),
                              (tgrp["Transacion_amount"].min(),tgrp["Transacion_amount"].max())),
                 hover_data=["Transacion_amount"], 
                fitbounds ="locations",basemap_visible=False,
                height =650, width =600).update_layout(title = dict(text=f"{year}'s {quater}Quater's All Transaction",font=dict(size=20, color='black'),x=0.5,y=0.9),
                                                       geo=dict(bgcolor= 'rgba(0,0,0,0)'),paper_bgcolor='rgba(0, 0, 0, 0)')
    fig_india.layout.coloraxis.colorbar.title = 'Transaction_Range'            
    st.plotly_chart(fig_india,use_container_width=True) 
       
## TOP TRANS PINCODES
def top_p(years,states):
    curr = conn.cursor()
    curr.execute(f"select Year,State,Pincodes,Transacion_count,Transacion_amount from  top_Trans where Year= {years} and State = '{states}';")
    table1 = curr.fetchall()
    pgrp =pd.DataFrame(table1,columns =["Year","State","Pincodes","Transacion_count","Transacion_amount"])
    #pgrp
    fig = px.bar(pgrp, x="Pincodes", y="Transacion_count",hover_name ="State",color='Transacion_amount',
                                color_continuous_scale='viridis').update_layout(
                        title = dict(text=f"{years}'s {states}'s Pincode wise Transaction",font=dict(size=20, color='black'),x=0.2,y=0.9),
                        xaxis_title=dict(text ='Pincodes',font=dict(size=10, color='black')),
                        yaxis_title=dict(text ='Transaction Count',font=dict(size=10, color='black')),plot_bgcolor='rgba(0, 0, 0, 0)',
                        paper_bgcolor='rgba(0, 0, 0, 0)')   
          
    st.plotly_chart(fig,use_container_width=True) 
    
 # Top User REgUser
def top_U(years):
    curr = conn.cursor()
    curr.execute(f"select Year,Quater,State,RegisteredUsers from  top_User where Year= {years};")
    table1 = curr.fetchall()
    pgrp =pd.DataFrame(table1,columns =["Year","Quater","State","RegisteredUsers"])
    #pgrp
    fig = px.bar(pgrp, x="State", y="RegisteredUsers",hover_name ="State",color='Quater',height= 800,
                                color_continuous_scale='viridis').update_layout(
                        title = dict(text=f"{years}'s Quater wise Registered Users",font=dict(size=20, color='black'),x=0.5,y=0.9),
                        transition={'duration': 3000000},
                         xaxis_title=dict(text ='State',font=dict(size=10, color='black')),
                        yaxis_title=dict(text ='RegisteredUsers',font=dict(size=10, color='black')),plot_bgcolor='rgba(0, 0, 0, 0)',
                        paper_bgcolor='rgba(0, 0, 0, 0)')          
    st.plotly_chart(fig,use_container_width=True) 
    
# top user pincode    
def top_Up(years,states):
    curr = conn.cursor()
    curr.execute(f"select Year,Quater,State,Pincodes,RegisteredUsers from  top_User where Year= {years} and State = '{states}';")
    table1 = curr.fetchall()
    pgrp =pd.DataFrame(table1,columns =["Year","Quater","State","Pincodes","RegisteredUsers"])
    #pgrp
    fig = px.bar(pgrp, x="Quater", y="RegisteredUsers",hover_data =["Pincodes"],color='RegisteredUsers',
                                color_continuous_scale='viridis').update_layout(
                        title = dict(text=f"{years}{states} pincodes wise Registered Users",font=dict(size=20, color='black'),x=0.2,y=0.9),
                        xaxis_title=dict(text ='State',font=dict(size=10, color='black')),
                        yaxis_title=dict(text ='RegisteredUsers',font=dict(size=10, color='black')),plot_bgcolor='rgba(0, 0, 0, 0)',
                        paper_bgcolor='rgba(0, 0, 0, 0)')          
    st.plotly_chart(fig,use_container_width=True) 
  
  #TAB 3 QUESTION
  # Q1  Amt  FUNC
def query(tab_name):  
    curr = conn.cursor()
    #Agg_Trans
    curr.execute(f'''select State,sum(Transacion_amount) as Transaction_Amount from {tab_name} group by State 
                    order by Transaction_Amount desc limit 10; ''')
    conn.commit()
    Q1 = curr.fetchall()
    q1 =pd.DataFrame(Q1,columns =["State","Transaction_Amount"])
    #q1
    col1,col2 = st.columns(2)
    with col1:
      fig = px.bar(q1, x="State", y="Transaction_Amount",hover_name ="State",height= 600,width= 650,
                                      color_continuous_scale='viridis').update_layout(
                                    title = dict(text="Top 10 Transaction_Amount",font=dict(size=20, color='black'),x=0.5,y=0.9),
                                    xaxis_title=dict(text ='State',font=dict(size=10, color='black')),
                                    yaxis_title=dict(text ='Transaction_Amount',font=dict(size=10, color='black')),
                                    plot_bgcolor='rgba(0, 0, 0, 0)',
                                  paper_bgcolor='rgba(0, 0, 0, 0)') 
      st.plotly_chart(fig,use_container_width=True)      
    # p2
    with col2:
      curr.execute(f'''select State,sum(Transacion_amount) as Transaction_Amount from {tab_name} group by State 
                      order by Transaction_Amount limit 10; ''')
      conn.commit()
      Q2 = curr.fetchall()
      q2 =pd.DataFrame(Q2,columns =["State","Transaction_Amount"])
      #q1
      fig = px.bar(q2, x="State", y="Transaction_Amount",hover_name ="State",height= 600,width= 650,
                                  color_discrete_sequence= px.colors.sequential.Agsunset).update_layout(
                                  title = dict(text="Least 10 Transaction_Amount",font=dict(size=20, color='black'),x=0.5,y=0.9),
                                  xaxis_title=dict(text ='State',font=dict(size=10, color='black')),
                                  yaxis_title=dict(text ='Transaction_Amount',font=dict(size=10, color='black')),
                                  plot_bgcolor='rgba(0, 0, 0, 0)',
                                  paper_bgcolor='rgba(0, 0, 0, 0)') 
      st.plotly_chart(fig,use_container_width=True)       

    # p3
    curr.execute(f'''select State,Avg(Transacion_amount) as Transaction_Amount from {tab_name} group by State 
                    order by Transaction_Amount; ''')
    conn.commit()
    Q3 = curr.fetchall()
    q3 =pd.DataFrame(Q3,columns =["State","Transaction_Amount"])
    #q1
    fig = px.bar(q3, x="State", y="Transaction_Amount",hover_name ="State",height= 800,
                                color_discrete_sequence= px.colors.sequential.Electric).update_layout(
                                title = dict(text="Average of Transaction_Amount",font=dict(size=20, color='black'),x=0.5,y=0.9),
                                xaxis_title=dict(text ='State',font=dict(size=10, color='black')),
                                yaxis_title=dict(text ='Transaction_Amount',font=dict(size=10, color='black')),
                                plot_bgcolor='rgba(0, 0, 0, 0)',
                                paper_bgcolor='rgba(0, 0, 0, 0)').update_yaxes(tickfont=dict(color='black',
                                                            size=14)).update_xaxes(tickfont=dict(color='black', size=10)) 
    st.plotly_chart(fig,use_container_width=True)     
    
#  Q1 count func
def query1(tab_name):  
    curr = conn.cursor()
    #Agg_Trans
    curr.execute(f'''select State,sum(Transacion_count) as Transaction_Count from {tab_name} group by State 
                    order by Transaction_Count desc limit 10; ''')
    conn.commit()
    Q1 = curr.fetchall()
    q1 =pd.DataFrame(Q1,columns =["State","Transaction_Count"])
    #q1
    col1,col2 = st.columns(2)
    with col1:
      fig = px.bar(q1, x="State", y="Transaction_Count",hover_name ="State",height= 600,width= 650,
                                      color_continuous_scale='viridis').update_layout(
                                    title = dict(text="Top 10 Transaction_Count",font=dict(size=20, color='black'),x=0.5,y=0.9),
                                    xaxis_title=dict(text ='State',font=dict(size=10, color='black')),
                                    yaxis_title=dict(text ='Transaction_Count',font=dict(size=10, color='black')),
                                    plot_bgcolor='rgba(0, 0, 0, 0)',
                                    paper_bgcolor='rgba(0, 0, 0, 0)') 
      st.plotly_chart(fig,use_container_width=True)        
    # p2
    with col2:
      curr.execute(f'''select State,sum(Transacion_count) as Transaction_Count from {tab_name} group by State 
                      order by Transaction_Count limit 10; ''')
      conn.commit()
      Q2 = curr.fetchall()
      q2 =pd.DataFrame(Q2,columns =["State","Transaction_Count"])
      #q1
      fig = px.bar(q2, x="State", y="Transaction_Count",hover_name ="State",height= 600,width= 650,
                                  color_discrete_sequence= px.colors.sequential.Agsunset).update_layout(
                                  title = dict(text="Least 10 Transaction_Count",font=dict(size=20, color='black'),x=0.5,y=0.9),
                                  xaxis_title=dict(text ='State',font=dict(size=10, color='black')),
                                  yaxis_title=dict(text ='Transaction_Count',font=dict(size=10, color='black')),
                                  plot_bgcolor='rgba(0, 0, 0, 0)',
                                  paper_bgcolor='rgba(0, 0, 0, 0)') 
      st.plotly_chart(fig,use_container_width=True)         

    # p3
    curr.execute(f'''select State,Avg(Transacion_count) as Transaction_Count from {tab_name} group by State 
                    order by Transaction_Count; ''')
    conn.commit()
    Q3 = curr.fetchall()
    q3 =pd.DataFrame(Q3,columns =["State","Transaction_Count"])
    #q1
    fig = px.bar(q3, x="State", y="Transaction_Count",hover_name ="State",height= 600,width= 650,
                                color_discrete_sequence= px.colors.sequential.Electric).update_layout(
                                title = dict(text="Average of Transaction_Count",font=dict(size=20, color='black'),x=0.5,y=0.9),
                                xaxis_title=dict(text ='State',font=dict(size=10, color='black')),
                                yaxis_title=dict(text ='Transaction_Count',font=dict(size=10, color='black')),
                                plot_bgcolor='rgba(0, 0, 0, 0)',
                                paper_bgcolor='rgba(0, 0, 0, 0)').update_yaxes(tickfont=dict(color='black',
                                                            size=14)).update_xaxes(tickfont=dict(color='black', size=10)) 
    st.plotly_chart(fig,use_container_width=True)     
    
## agg user brands
def query2(tab_name):  
    curr = conn.cursor()
    #Agg_Trans
    curr.execute(f'''select Brands,sum(Percentage) as Percentage from {tab_name} group by Brands
                    order by Percentage desc limit 10;  ''')
    conn.commit()
    Q1 = curr.fetchall()
    q1 =pd.DataFrame(Q1,columns =["Brands","Percentage"])
    #q1
    col1,col2 = st.columns(2)
    with col1:
      fig = px.bar(q1, x="Brands", y="Percentage",hover_name ="Brands",height= 600,
                                      color_continuous_scale='viridis').update_layout(
                                    title = dict(text="Top 10 Brands",font=dict(size=20, color='black'),x=0.5,y=0.9),
                                    xaxis_title=dict(text ='Brands',font=dict(size=10, color='black')),
                                    yaxis_title=dict(text ='Percentage',font=dict(size=10, color='black')),
                                    plot_bgcolor='rgba(0, 0, 0, 0)',
                                    paper_bgcolor='rgba(0, 0, 0, 0)') 
    st.plotly_chart(fig,use_container_width=True)       
    # p2
    with col2:
      curr.execute(f'''select Brands,sum(Percentage) as Percentage from {tab_name} group by Brands
                      order by Percentage limit 10; ''')
      conn.commit()
      Q2 = curr.fetchall()
      q2 =pd.DataFrame(Q2,columns =["Brands"," Percentage"])
      #q1
      fig = px.bar(q2, x="Brands", y=" Percentage",hover_name ="Brands",height= 600,width= 650,
                                  color_discrete_sequence= px.colors.sequential.Agsunset).update_layout(
                                  title = dict(text="Least 10 Brands",font=dict(size=20, color='black'),x=0.5,y=0.9),
                                  xaxis_title=dict(text ='Brands',font=dict(size=10, color='black')),
                                yaxis_title=dict(text =' Percentage',font=dict(size=10, color='black')),
                                plot_bgcolor='rgba(0, 0, 0, 0)',
                                paper_bgcolor='rgba(0, 0, 0, 0)') 
    st.plotly_chart(fig,use_container_width=True)         

    # p3
    curr.execute(f'''select Brands,avg(Percentage) as Percentage from {tab_name} group by Brands
                    order by Percentage; ''')
    conn.commit()
    Q3 = curr.fetchall()
    q3 =pd.DataFrame(Q3,columns =["Brands"," Percentage"])
    #q1
    fig = px.bar(q3, y="Brands", x=" Percentage",hover_name ="Brands",height= 600,width= 650,
                                color_discrete_sequence= px.colors.sequential.Magenta_r).update_layout(
                                title = dict(text="Average of Brands percentage",font=dict(size=20, color='black'),x=0.5,y=1.0),
                                xaxis_title=dict(text ='Percentage',font=dict(size=10, color='black')),
                                yaxis_title=dict(text ='Brands',font=dict(size=10, color='black')),
                                plot_bgcolor='rgba(0, 0, 0, 0)',
                                paper_bgcolor='rgba(0, 0, 0, 0)').update_yaxes(tickfont=dict(color='black',
                                                            size=14)).update_xaxes(tickfont=dict(color='black', size=10)) 
    st.plotly_chart(fig,use_container_width=True)      
## MAP USER REG FUNC
def query3(tab_name,states):  
    curr = conn.cursor()
    #Agg_Trans
    curr.execute(f'''select Districts,sum(RegisteredUsers) as Registered_Users from {tab_name} where State = '{states}'
                   group by districts Order by Registered_Users desc limit 10 ;''')
    conn.commit()
    Q1 = curr.fetchall()
    q1 =pd.DataFrame(Q1,columns =["Districts","Registered_Users"])
    #q1
    col1,col2 = st.columns(2)
    with col1:
        fig = px.bar(q1, x="Districts", y="Registered_Users",hover_name ="Districts",height= 600,
                                    color_continuous_scale='viridis').update_layout(
                                   title = dict(text="Top 10 Registered_Users",font=dict(size=20, color='black'),x=0.5,y=0.9),
                                   xaxis_title=dict(text ='Districts',font=dict(size=10, color='black')),
                                   yaxis_title=dict(text ='Registered_Users',font=dict(size=10, color='black')),
                                  plot_bgcolor='rgba(0, 0, 0, 0)',
                                  paper_bgcolor='rgba(0, 0, 0, 0)') 
    st.plotly_chart(fig,use_container_width=True)       
    # p2
    with col2:
        curr.execute(f'''select Districts,sum(RegisteredUsers) as Registered_Users from {tab_name} where State = '{states}'
                    group by districts Order by Registered_Users limit 10;''')
        conn.commit()
        Q2 = curr.fetchall()
        q2 =pd.DataFrame(Q2,columns =["Districts","Registered_Users"])
        #q1
        fig = px.bar(q2, x="Districts", y="Registered_Users",hover_name ="Districts",height= 600,width= 650,
                                    color_discrete_sequence= px.colors.sequential.Agsunset).update_layout(
                                title = dict(text="Least 10 Registered_Users",font=dict(size=20, color='black'),x=0.5,y=0.9),
                                xaxis_title=dict(text ='Districts',font=dict(size=10, color='black')),
                                yaxis_title=dict(text ='Registered_Users',font=dict(size=10, color='black')),
                                plot_bgcolor='rgba(0, 0, 0, 0)',
                                paper_bgcolor='rgba(0, 0, 0, 0)') 
    st.plotly_chart(fig,use_container_width=True)         

    # p3
    curr.execute(f'''select Districts,Avg(RegisteredUsers) as Registered_Users from {tab_name} where State = '{states}'
  group by districts Order by Registered_Users limit 10;''')
    conn.commit()
    Q3 = curr.fetchall()
    q3 =pd.DataFrame(Q3,columns =["Districts","Registered_Users"])
    #q1
    fig = px.bar(q3, y="Districts", x="Registered_Users",hover_name ="Districts",height= 600,width= 650,
                                color_discrete_sequence= px.colors.sequential.Emrld_r).update_layout(
                                title = dict(text="Average of Registered_Users",font=dict(size=20, color='black'),x=0.5,y=1.0),
                                xaxis_title=dict(text ='Registered_Users',font=dict(size=10, color='black')),
                                yaxis_title=dict(text ='Districts',font=dict(size=10, color='black')),
                                plot_bgcolor='rgba(0, 0, 0, 0)',
                                paper_bgcolor='rgba(0, 0, 0, 0)') 
    st.plotly_chart(fig,use_container_width=True)                                                                     

# map User appopens
def query4(tab_name,states):  
    curr = conn.cursor()
    #Agg_Trans
    curr.execute(f'''select Districts,sum(AppOpens) as AppOpens from {tab_name} where State = '{states}'
                   group by districts Order by AppOpens desc limit 10 ;''')
    conn.commit()
    Q1 = curr.fetchall()
    q1 =pd.DataFrame(Q1,columns =["Districts","AppOpens"])
    #q1
    col1,col2 = st.columns(2)
    with col1:
       fig = px.line(q1, x="Districts", y="AppOpens",hover_name ="Districts",height= 600,
                                    color_discrete_sequence=px.colors.sequential.Magenta_r,markers="*").update_layout(
                                   title = dict(text="Top 10 AppOpens",font=dict(size=20, color='black'),x=0.5,y=0.9),
                                   xaxis_title=dict(text ='Districts',font=dict(size=10, color='black')),
                                   yaxis_title=dict(text ='AppOpens',font=dict(size=10, color='black')),plot_bgcolor='rgba(0, 0, 0, 0)',
                                  paper_bgcolor='rgba(0, 0, 0, 0)').update_yaxes(tickfont=dict(color='black',
                                                            size=14)).update_xaxes(tickfont=dict(color='black', size=14))
                                     
    st.plotly_chart(fig,use_container_width=True)       
    # p2
    with col2:
        curr.execute(f'''select Districts,sum(AppOpens) as AppOpens from {tab_name} where State = '{states}'
                    group by districts Order by AppOpens limit 10;''')
        conn.commit()
        Q2 = curr.fetchall()
        q2 =pd.DataFrame(Q2,columns =["Districts","AppOpens"])
        #q1
        fig = px.line(q2, x="Districts", y="AppOpens",hover_name ="Districts",height= 600,width= 650,markers="*",
                                    color_discrete_sequence= px.colors.sequential.Agsunset).update_layout(
                                title = dict(text="Least 10 AppOpens",font=dict(size=20, color='black'),x=0.5,y=0.9),
                                xaxis_title=dict(text ='Districts',font=dict(size=10, color='black')),
                                yaxis_title=dict(text ='AppOpens',font=dict(size=10, color='black')),
                                plot_bgcolor='rgba(0, 0, 0, 0)',
                                paper_bgcolor='rgba(0, 0, 0, 0)').update_yaxes(tickfont=dict(color='black',
                                                            size=14)).update_xaxes(tickfont=dict(color='black', size=14))
       
    st.plotly_chart(fig,use_container_width=True)        

    # p3
    curr.execute(f'''select Districts,Avg(AppOpens) as AppOpens from {tab_name} where State = '{states}'
                  group by districts Order by AppOpens;''')
    conn.commit()
    Q3 = curr.fetchall()
    q3 =pd.DataFrame(Q3,columns =["Districts","AppOpens"])
    #q1
    fig = px.line(q3, y="Districts", x="AppOpens",hover_name ="Districts",height= 600,markers="*",
                                color_discrete_sequence= px.colors.sequential.Emrld_r).update_layout(
                                title = dict(text="Average of AppOpens",font=dict(size=20, color='black'),x=0.5,y=1.0),
                                xaxis_title=dict(text ='AppOpens',font=dict(size=10, color='black')),
                                yaxis_title=dict(text ='Districts',font=dict(size=10, color='black')),
                                plot_bgcolor='rgba(0, 0, 0, 0)',
                                paper_bgcolor='rgba(0, 0, 0, 0)').update_yaxes(tickfont=dict(color='black',
                                                            size=14)).update_xaxes(tickfont=dict(color='Black', size=14))
                                     
    st.plotly_chart(fig,use_container_width=True) 
    
## top  user func
def query5(tab_name):  
    curr = conn.cursor()
    #Agg_Trans
    curr.execute(f'''select State,sum(RegisteredUsers) as Registered_Users from {tab_name}
                   group by State Order by Registered_Users desc limit 10 ;''')
    conn.commit()
    Q1 = curr.fetchall()
    q1 =pd.DataFrame(Q1,columns =["State","Registered_Users"])
    #q1
    col1,col2 = st.columns(2)
    with col1:
        fig = px.line(q1, x="State", y="Registered_Users",hover_name ="State",height= 600,width= 650,markers="*",
                                     color_discrete_sequence= px.colors.sequential.Blues_r).update_layout(
                                   title = dict(text="Top 10 Registered_Users",font=dict(size=20, color='black'),x=0.5,y=0.9),
                                   xaxis_title=dict(text ='State',font=dict(size=10, color='black')),
                                   yaxis_title=dict(text ='Registered_Users',font=dict(size=10, color='black')),
                                  plot_bgcolor='rgba(0, 0, 0, 0)',
                                  paper_bgcolor='rgba(0, 0, 0, 0)').update_yaxes(tickfont=dict(color='black',
                                                            size=14)).update_xaxes(tickfont=dict(color='black', size=14)) 
    st.plotly_chart(fig,use_container_width=True)       
    # p2
    with col2:
        curr.execute(f'''select State,sum(RegisteredUsers) as Registered_Users from {tab_name}
                    group by State Order by Registered_Users limit 10;''')
        conn.commit()
        Q2 = curr.fetchall()
        q2 =pd.DataFrame(Q2,columns =["State","Registered_Users"])
        #q1
        fig = px.line(q2, x="State", y="Registered_Users",hover_name ="State",height= 600,markers="*",
                                    color_discrete_sequence= px.colors.sequential.Agsunset).update_layout(
                                title = dict(text="Least 10 Registered_Users",font=dict(size=20, color='black'),x=0.5,y=0.9),
                                xaxis_title=dict(text ='State',font=dict(size=10, color='black')),
                                yaxis_title=dict(text ='Registered_Users',font=dict(size=10, color='black')),
                                plot_bgcolor='rgba(0, 0, 0, 0)',
                                paper_bgcolor='rgba(0, 0, 0, 0)').update_yaxes(tickfont=dict(color='black',
                                                            size=14)).update_xaxes(tickfont=dict(color='black', size=14)) 
    st.plotly_chart(fig,use_container_width=True)       

    # p3
    curr.execute(f'''select State,Avg(RegisteredUsers) as Registered_Users from {tab_name}
                         group by State Order by Registered_Users;''')
    conn.commit()
    Q3 = curr.fetchall()
    q3 =pd.DataFrame(Q3,columns =["State","Registered_Users"])
    #q1
    fig = px.line(q3, y="State", x="Registered_Users",hover_name ="State",height= 600,width= 650,markers="*",
                                color_discrete_sequence= px.colors.sequential.Emrld_r).update_layout(
                                title = dict(text="Average of Registered_Users",font=dict(size=20, color='black'),x=0.5,y=1.0),
                                xaxis_title=dict(text ='Registered_Users',font=dict(size=10, color='black')),
                                yaxis_title=dict(text ='State',font=dict(size=10, color='black')),
                                plot_bgcolor='rgba(0, 0, 0, 0)',
                                paper_bgcolor='rgba(0, 0, 0, 0)').update_yaxes(tickfont=dict(color='black',
                                                            size=14)).update_xaxes(tickfont=dict(color='black', size=14))
       
    st.plotly_chart(fig,use_container_width=True)   
    
                                        
                                        
    
#streamlit part

st.set_page_config(layout="wide")
 
with open(r'C:\Users\Admin\OneDrive\Desktop\phonepe\style1.css') as f:
  st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)
     
with st.sidebar:
    st.title(" :violet[WELCOME TO MY PROJECT]")
    st.header("skill Take Away" ,divider='rainbow')
    st.caption(":blue[_python Scripting_]")
    st.caption(":blue[_Data Exploration_]")
    st.caption(":blue[_Data Visualization_]")
    st.caption(":blue[_Data Management using sqlite3_]")
    st.caption(":blue[_Building Streamlit_]")     
          
tab1,tab2,tab3 = st.tabs([":black[Home]",":black[🌍 Data Exploration]",":black[📈 Data Visualization]"])
with tab1:
  st.title(":blue[PHONEPE DATA VISUALISATION AND EXPLORATION]:female-detective:")
  col1,col2 = st.columns(2)
  with col1:
    st.header(":violet[PhonePe]")
    
    st.image("C:/Users/Admin/OneDrive/Desktop/phonepe/phonepe_1.ico.png", caption="keep it simple with phonepe!", 
              width=100, use_column_width=100, clamp=False,
              channels="RGB", output_format="icon")   
  with col2:  
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    
    st.subheader(":violet[_INDIA's BEST TRANSACTION APP_]")
    
    st.markdown("PhonePe  is an Indian digital payments and financial technology company")
  
  col1,col2 = st.columns(2)
  with col1:
    st.markdown(" ")
    st.markdown(" ")
    st.write(":violet[_****FEATURES****_]")
    st.markdown(" ")
    st.write("****Credit & Debit card linking****")
    st.write("****Bank Balance check****")
    st.write("****Money Storage****")
    st.write("****PIN Authorization****")
    
  col1,col2 = st.columns(2)
  with col1:
    st.write("****Easy Transactions****")
    st.write("****One App For All Your Payments****")
    st.write("****Your Bank Account Is All You Need****")
    st.write("****Multiple Payment Modes****")
    st.write("****PhonePe Merchants****")
    st.write("****Multiple Ways To Pay****")
    st.write("****1.Direct Transfer & More****")
    st.write("****2.QR Code****")
    st.write("****Earn Great Rewards****")
  with col2:
    st.image("https://cdn.dribbble.com/users/2534929/screenshots/9519641/phonepe-800x600.gif", caption=None, 
              width=None, use_column_width=None, clamp=False,
              channels="RGB", output_format="auto")   
    
  col3,col4 = st.columns(2)
  with col3: 
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.link_button(":violet[DOWNLOAD THE APP NOW]","https://play.google.com/store/apps/details?id=com.phonepe.app&hl=en_IN")
    #"https://www.phonepe.com/app-download/")   
    
  with col4:  
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.write("****No Wallet Top-Up Required****")
    st.write("****Pay Directly From Any Bank To Any Bank A/C****")
    st.write("****Instantly & Free****") 
 
  
with tab2:
  select = option_menu(menu_title = None,icons = None,
                       options=["Aggregated Analysis","Map Analysis","Top Analysis"], default_index=0, orientation="horizontal")
    
  if select == "Aggregated Analysis":
    method =st.radio("select the method",["Transaction Analysis","User Analysis"])  
    if method =="Transaction Analysis":
      years =st.slider("Select the Year:",2018,2024,2018)
      col1,col2 = st.columns(2)
      with col1:
        pass
      tac1 = tac_Y(years)
      #slider for quaters
      quater =st.slider("Select the Quarter:",1,4,1)
      col1,col2 = st.columns(2)
      with col1:
        pass
      tac_Q(years,quater)
      #trans types
      states = st.selectbox("Select the State:",('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                                                  'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                                  'Dadra and Nagarhaveli and Daman  and Diu', 'Delhi', 'Goa',
                                                  'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                                  'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                                  'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                                  'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                                  'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                                  'Uttarakhand', 'West Bengal'))
      tac_T(years,states)
      
    elif method == "User Analysis":
      years =st.slider("Select the Year:",2018,2022,2018)
      ubc_Y(years)
      
      quater =st.slider("Select the Quarter:",1,4,1)
      ubc_Q(years,quater)
      
      ubc_S(years)
    
 ## MAP ANALYSIS     
          
  if select == "Map Analysis":
    method =st.radio("select the method",["Transaction Analysis","User Analysis"])  
    if method =="Transaction Analysis":
      years =st.slider(":Black[SELECT YOUR YEAR:]",2018,2024,2018) 
      
      map_Y(years)
        #slider for quaters
      quater =st.slider(":Black[SELECT YOUR QUARTER:]",1,4,1)
      map_Q(years,quater)
          #districts box
      states =st.selectbox(":Black[SELECT YOUR STATE:]",('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                                                  'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                                  'Dadra and Nagarhaveli and Daman  and Diu', 'Delhi', 'Goa',
                                                  'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                                  'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                                  'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                                  'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                                  'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                                  'Uttarakhand', 'West Bengal'))
      map_D(years,states)
      # map user analysis
    elif method == "User Analysis":
      years =st.slider("Select the Year:",2018,2024,2018)
      mu_Y(years)
      #QUATER FUNC
      mu_Q(years)
      app(years)
      
  if select == "Top Analysis":
    method =st.radio("select the method",["Transaction Analysis","User Analysis"])  
    if method =="Transaction Analysis":
      years =st.slider("Select the Year:",2018,2024,2018)
      top_Y(years)
      #slider for quaters
      quater =st.slider("Select the Quarter:",1,4,1)
      top_Q(years,quater)
      # pincode
      states =st.selectbox(":Black[SELECT YOUR STATE:]",('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                                                  'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                                  'Dadra and Nagarhaveli and Daman  and Diu', 'Delhi', 'Goa',
                                                  'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                                  'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                                  'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                                  'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                                  'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                                  'Uttarakhand', 'West Bengal'))
      
      top_p(years,states)
      # top user
    elif method == "User Analysis":
      years =st.slider("Select the Year:",2018,2024,2018)
      top_U( years)
      # pincode
      states =st.selectbox(":Black[SELECT YOUR STATE:]",('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                                                  'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                                  'Dadra and Nagarhaveli and Daman  and Diu', 'Delhi', 'Goa',
                                                  'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                                  'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                                  'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                                  'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                                  'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                                  'Uttarakhand', 'West Bengal')) 
      top_Up(years,states)
  
with tab3:
  st.header(":blue[_SELECT YOUR QUESTION:_]")
  question = st.selectbox("",("1.Transaction Amount and Count of Aggregated Transaction",
                                                "2.Transaction Amount of Map Transaction",
                                                "3.Transaction Amount of Top Transaction",
                                                "4.Transaction Count of Aggregated User",
                                                "5.Brands and percentage of Aggregated User", 
                                                "6.Registered users of Map User",
                                                "7.App opens of Map User",
                                                "8.Registered users of Top User",
                                                "9.Transaction Count of Map Transaction",
                                                "10.Transaction Count of Top Transaction"))
  
  if question == "1.Transaction Amount and Count of Aggregated Transaction":        
     st.subheader(":violet[_Transaction Amount visuals:_]")
     query("Agg_Trans") 
     st.subheader(":violet[_Transaction Count visuals:_]")
     query1("Agg_Trans")                                        
  
  elif question == "2.Transaction Amount of Map Transaction":        
     st.subheader(":violet[_Transaction Amount visuals:_]")
     query("map_Trans") 
     
  elif question == "3.Transaction Amount of Top Transaction":        
      st.subheader(":violet[_Transaction Amount visuals:_]")
      query("top_Trans") 
     
  elif question == "4.Transaction Count of Aggregated User":        
      st.subheader(":violet[_Transaction Count visuals:_]")
      query1("Agg_User") 
     
  elif question == "5.Brands and percentage of Aggregated User":        
      st.subheader(":violet[_Brands visuals:_]")
      query2("Agg_User")     
     
  elif question == "6.Registered users of Map User":        
      st.subheader(":violet[_District Wise visuals:_]")
      states =st.selectbox(":Black[SELECT YOUR STATES:]",('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                                                  'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                                  'Dadra and Nagarhaveli and Daman  and Diu', 'Delhi', 'Goa',
                                                  'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                                  'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                                  'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                                  'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                                  'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                                  'Uttarakhand', 'West Bengal')) 
      query3("map_User",states)
      
  elif question == "7.App opens of Map User":        
      st.subheader(":violet[_App opens visuals:_]")
      states =st.selectbox(":Black[SELECT YOUR STATE's:]",('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                                                  'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                                  'Dadra and Nagarhaveli and Daman  and Diu', 'Delhi', 'Goa',
                                                  'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                                  'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                                  'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                                  'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                                  'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                                  'Uttarakhand', 'West Bengal')) 
      query4("map_User",states)   
       
  elif question == "8.Registered users of Top User":        
      st.subheader(":violet[_Registered user visuals:_]")
      query5("top_User")
      
  elif question == "9.Transaction Count of Map Transaction":        
      st.subheader(":violet[_Transaction Count visuals:_]")
      query1("map_Trans") 
      
  elif question == "10.Transaction Count of Top Transaction":        
      st.subheader(":violet[_Transaction Count visuals:_]")
      query1("top_Trans")            


    
    
    