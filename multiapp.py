import streamlit as st

class Multiapp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        logo = './images/ird-logo-long.png'
        
        with st.sidebar:
            # st.image(logo)
            app = st.selectbox(
                'Navigation',
                self.apps,
                format_func = lambda app: app['title'])

        

        app['function']()