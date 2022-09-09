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
        ## Un modèle NER pour l'extraction des organes et descripteurs
        """)
        
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)

    with st.sidebar:
        choices = {
            'Modèle v2 (549 organes, 998 descripteurs, 856 rows)': './ner-models/ner-all-model-double-upgraded',
            'Modèle v1 (141 organes, 1004 descripteurs, 856 rows)': './ner-models/ner-descripteurs-organes-model-grpd'
        }
        output_choice = ['Highlighted', 'Vue table']

        model_choice = st.selectbox('Version du modèle', choices.keys())
        output_format = st.selectbox("Format de l'output", output_choice)
        

    nlp = spacy.load(choices[model_choice])
    example_text = "grandes feuilles opposées, oblongues-elliptiques ou obovées-elliptiques, arrondies au sommet, obtuses ou cunéiformes à la base  limbe glabre, mesurant jusqu'à 20 cm de longueur sur 12 cm de largeur  nervure médiane proéminente dessous, un peu saillante dessus  nervures secondaires, 5 à 10 paires, incurvées, réunies en arceaux assez loin de la marge, saillantes dessous, bien marquées dessus, anastomosées à un réseau de nervilles à grosses mailles irrégulières, finement saillant dessus  pétiole 5-20 mm  fleurs blanches fasciculées sur le vieux bois  pédicelle 4-6 mm, glabre ou légèrement pubescent  galice : 4 sépales (2 + 2) de 2,5 mm, un peu pubes-cents extérieurement  corolle à 8 lobes de 3 mm; tube 2 mm  ëtamines 8, insérées à la gorge; filets 3 mm  ovaire velu, à 4 loges, prolongé d'un long style glabre  dans le bouton la corolle, étroitement fermée, laisse poindre très apparemment le style  fruits inconnus  le spécimen type renferme une seule graine fusiforme non carénée, de 2 cm long, 0,6 large, 0,6 épaisseur, à cicatrice oblongue coupant toute la face ventrale, à bords crénelés"
    text = st.text_area("Entrer du texte ici",example_text)
    HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""
    
    if text:
        doc = nlp(text.lower())
        

        if output_format == 'Highlighted':
            colors = {'ORGANE': "#cdcd00", "DESCRIPTEUR": "#85C1E9"}
            options = {"ents": ['ORGANE', 'DESCRIPTEUR'], "colors": colors}


            html = displacy.render(doc,style="ent", options=options)
            html = html.replace("\n\n","\n")
            st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)
        
        elif output_format == 'Vue table':
            st.markdown("""
                ### Vue table: Descripteurs par organe
                Chaque terme `DESCRIPTEUR` est associé au terme `ORGANE` qu'il précède.
            """)

            organes = {}
            org = ""
            for ent in doc.ents:
                if ent.label_ == 'ORGANE':
                    org = ent.text
                    organes[org] = []  
                else:
                    organes[org].append(ent.text)

            for o in organes.keys():
                organes[o] = ", ".join(organes[o])

            df_out = pd.DataFrame(organes.items(), columns=['ORGANE', 'DESCRIPTEUR'])
            st.dataframe(df_out)

        