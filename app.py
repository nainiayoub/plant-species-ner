import streamlit as st
import spacy
from spacy import displacy

st.set_page_config(layout="wide")

html_temp = """
                <div style="background-color:{};padding:1px">
                
                </div>
                """



with st.sidebar:
    pages = st.selectbox('Pages', ['Extraction des espèces', 'Extraction des organes et descripteurs'])


if pages == 'Extraction des espèces':
    st.markdown("""
    ## Un modèle NER pour l'extraction des espèces de plantes
    """)
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
    choices = {
        'Modèle v2 (2425 data rows)': './ner-species-model-close-recent',
        'Modèle v1 (1449 data rows)': './ner-species-model-recent'
    }
    model_choice = st.selectbox('Choix du modèle NER', choices.keys())
        
    nlp = spacy.load(choices[model_choice])
    example_text = "Oxera subverticillata est une liane robuste de forêt dense humide, largement répartie du centre au nord de la Grande Terre. Espèce assez commune avec une zone d'occurrence (EOO) de 3651 km² et une zone d'occupation de 100 km², O. subverticillata est évalué en Préoccupation Mineure (LC)."
    text = st.text_area("Entrer du texte ici",example_text)
    HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""
    if text:
        doc = nlp(text)
        html = displacy.render(doc,style="ent")
        html = html.replace("\n\n","\n")
        st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)

elif pages == 'Extraction des organes et descripteurs':
    st.markdown("""
    ## Un modèle NER pour l'extraction des organes et descripteurs
    """)
    
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
    choices = {
        
        'Modèle v1 (141 organes, 1004 descripteurs, 856 rows)': './ner-descripteurs-organes-model-grpd',
        'Modèle v2 (549 organes, 998 descripteurs, 856 rows)': './ner-all-model-double-upgraded',
    }
    model_choice = st.selectbox('Choix du modèle NER', choices.keys())
        
    nlp = spacy.load(choices[model_choice])
    example_text = "grandes feuilles opposées, oblongues-elliptiques ou obovées-elliptiques, arrondies au sommet, obtuses ou cunéiformes à la base  limbe glabre, mesurant jusqu'à 20 cm de longueur sur 12 cm de largeur  nervure médiane proéminente dessous, un peu saillante dessus  nervures secondaires, 5 à 10 paires, incurvées, réunies en arceaux assez loin de la marge, saillantes dessous, bien marquées dessus, anastomosées à un réseau de nervilles à grosses mailles irrégulières, finement saillant dessus  pétiole 5-20 mm  fleurs blanches fasciculées sur le vieux bois  pédicelle 4-6 mm, glabre ou légèrement pubescent  galice : 4 sépales (2 + 2) de 2,5 mm, un peu pubes-cents extérieurement  corolle à 8 lobes de 3 mm; tube 2 mm  ëtamines 8, insérées à la gorge; filets 3 mm  ovaire velu, à 4 loges, prolongé d'un long style glabre  dans le bouton la corolle, étroitement fermée, laisse poindre très apparemment le style  fruits inconnus  le spécimen type renferme une seule graine fusiforme non carénée, de 2 cm long, 0,6 large, 0,6 épaisseur, à cicatrice oblongue coupant toute la face ventrale, à bords crénelés"
    text = st.text_area("Entrer du texte ici",example_text)
    HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""
    
    if text:
        doc = nlp(text.lower())
        colors = {'ORGANE': "#cdcd00", "DESCRIPTEUR": "#85C1E9"}
        options = {"ents": ['ORGANE', 'DESCRIPTEUR'], "colors": colors}


        html = displacy.render(doc,style="ent", options=options)
        html = html.replace("\n\n","\n")
        st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)

