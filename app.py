
import streamlit as st
from multiapp import Multiapp
from pages import especes, termes

logo = './images/logo-IRD.png'
st.set_page_config(layout="wide", page_title="Extraction automatique d'informations botaniques")



app = Multiapp()

app.add_app("Extraction des espèces", especes.app)
app.add_app("Extraction des organes et des descripteurs", termes.app)



app.run()