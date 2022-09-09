import streamlit as st
import spacy
from spacy import displacy
import pandas as pd

def app():

    html_temp = """
                    <div style="background-color:{};padding:1px">
                    
                    </div>
                    """

    st.markdown("""
    ## Un modèle NER pour l'extraction des espèces de plantes
    """)
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
    st.markdown("""
        Dans la botanique, chaque espèce est doté d'un nom binomial qui se compose du nom scientifique du genre et d'une épithète spécifique qui décrit l'espèce. 
        Ce modèle permet d'extraire les noms d'espèces botaniques à partir de description textuelle.
        """)
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
    
    with st.sidebar:
        
        choices = {
            'Modèle v2 (2425 data rows)': './ner-models/ner-species-model-close-recent',
            'Modèle v1 (1449 data rows)': './ner-models/ner-species-model-recent'
        }
        model_choice = st.selectbox('Version du modèle NER', choices.keys())

        
        
    nlp = spacy.load(choices[model_choice])
    example_text = "Oxera subverticillata est une liane robuste de forêt dense humide, largement répartie du centre au nord de la Grande Terre. Espèce assez commune avec une zone d'occurrence (EOO) de 3651 km² et une zone d'occupation de 100 km², O. subverticillata est évalué en Préoccupation Mineure (LC)."
    text = st.text_area("Entrer du texte ici",example_text)
    HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""
    if text:
        doc = nlp(text)
        html = displacy.render(doc,style="ent")
        html = html.replace("\n\n","\n")
        st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)
        
            

