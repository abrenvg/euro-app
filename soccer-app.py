import streamlit as st
import pandas as pd
import json
from mplsoccer import VerticalPitch
st.title("Euros 2024 shot map")
st.subheader("Filter to any team/player to see all their shots taken!!")
df=pd.read_csv('euros_2024_shot_map.csv')
# print(df.head())
df=df[df['type']=='Shot'].reset_index(drop=True)
df['location']=df['location'].apply(json.loads)#convert string object of coordinates to list obj

team=st.selectbox('Select a team',df['team'].sort_values().unique(),index=None)#to create a dropdown to select teams
player=st.selectbox('Select a player',df[df['team']==team]['player'].sort_values().unique(),index=None)# create a dropdown for players only in selected team,index=none -i.e no default player is selected

def filter(df,team,player):
    if team:
        df=df[df['team']==team]
    if player:
        df=df[df['player']==player]
    return df

filtered_df=filter(df,team,player)

pitch=VerticalPitch(pitch_type='statsbomb',half=True)
fig,ax=pitch.draw(figsize=(10,10))

def plot_shots(df,ax,pitch):
    for x in df.to_dict(orient='records'):
        pitch.scatter(

            x=float(x['location'][0]),
            y=float(x['location'][1]),
            ax=ax,
            s=300*x['shot_statsbomb_xg'] if x['shot_outcome']=='Goal' else 500*x['shot_statsbomb_xg'] ,
            color='green' if x['shot_outcome']=='Goal' else 'red',
            edgecolors='black',
            alpha=1 if x['type']=='goal' else .5,
            zorder=2 if x['type']=='goal' else 1,
       )
        
plot_shots(filtered_df,ax,pitch)



st.pyplot(fig)

