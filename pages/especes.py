import streamlit as st
import spacy
from spacy import displacy
import pandas as pd
import csv 

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
    # st.warning("Dans la botanique, chaque espèce est doté d'un nom binomial qui se compose du nom scientifique du genre et d'une épithète spécifique qui décrit l'espèce. Ce modèle permet d'extraire les noms d'espèces botaniques à partir de description textuelle.")
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
    HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 1rem">{}</div>"""
    if text:
        doc = nlp(text)
        html = displacy.render(doc,style="ent")
        html = html.replace("\n\n","\n")
        with st.expander("Affichage NER"):
            st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)

        with st.expander("Etendre l'ensemble de données"):
            st.markdown("""
            ### Améliorer le modèle: Etendre l'ensemble de données
            """)
            st.warning("Pour étendre l'ensemble de données d'entraînement, l'utilisateur peut enregistrer le texte d'entrée avec ses entités nommées, présentes et manquantes, de type ESPECE.")
    
            # st.markdown("""
            # #### Texte botanique d'entrée
            # """)
            # st.write(text)

            # st.markdown("""
            # #### Les entités nommées de type __ESPECE__
            # """)
            
            present_named_entities = [e.text for e in doc.ents]
            str_present_named_entities = ', '.join(present_named_entities)
            named_entities = st.text_input('Ajouter les entités nommées manquantes en les séparant par une virgule', str_present_named_entities)
            fields = [text, named_entities]
            r = pd.read_csv('./data/data.csv')
            if st.button('Ajouter comme ligne de données'):
                with open('./data/data.csv', 'a', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f, delimiter=',', lineterminator='\n')
                    writer.writerow(fields)

            r = pd.read_csv('./data/data.csv')
            st.table(r)

