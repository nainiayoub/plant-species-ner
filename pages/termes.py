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
    ## Un modèle NER pour l'extraction des termes morphologiques: ORGANE et DESCRIPTEUR
    """)
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
    st.markdown("""
    La morphologie végétale est la partie de la botanique qui consiste à décrire la forme et la structure externe des plantes et de leurs organes. 
    Ce modèle permet d'extraire les termes morphologiques d'une description d'espèce, notament les ___organes___ et les ___descripteurs___, d'une manière grossière.
    """)
    # st.warning("La morphologie végétale est la partie de la botanique qui consiste à décrire la forme et la structure externe des plantes et de leurs organes. Ce modèle permet d'extraire les termes morphologiques d'une description d'espèce, notament les ___organes___ et les ___descripteurs___, d'une manière grossière.")
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)

    with st.sidebar:
        choices = {
            'Modèle v3':'./ner-models/ner-all-model-20_09_2022',
            'Modèle v4 (fine-grained)':'./ner-models/ner-model-precise-09-10-22',
            'Modèle v4 (fine-grained updated)': './ner-models/ner-model-precise-12-10-22',
            'Modèle v2 (549 organes, 998 descripteurs, 856 rows)': './ner-models/ner-all-model-double-upgraded',
            'Modèle v1 (141 organes, 1004 descripteurs, 856 rows)': './ner-models/ner-descripteurs-organes-model-grpd'
        }
        model_choice = st.selectbox('Version du modèle', choices.keys())

        output_choice = ['Highlighted', 'Vue dataframe', 'Vue dictionnaire']
        output_format = st.selectbox("Format de l'output", output_choice)
        
        

    nlp = spacy.load(choices[model_choice])
    example_text = "grandes feuilles opposées, oblongues-elliptiques ou obovées-elliptiques, arrondies au sommet, obtuses ou cunéiformes à la base  limbe glabre, mesurant jusqu'à 20 cm de longueur sur 12 cm de largeur  nervure médiane proéminente dessous, un peu saillante dessus  nervures secondaires, 5 à 10 paires, incurvées, réunies en arceaux assez loin de la marge, saillantes dessous, bien marquées dessus, anastomosées à un réseau de nervilles à grosses mailles irrégulières, finement saillant dessus  pétiole 5-20 mm  fleurs blanches fasciculées sur le vieux bois  pédicelle 4-6 mm, glabre ou légèrement pubescent  galice : 4 sépales (2 + 2) de 2,5 mm, un peu pubes-cents extérieurement  corolle à 8 lobes de 3 mm; tube 2 mm  ëtamines 8, insérées à la gorge; filets 3 mm  ovaire velu, à 4 loges, prolongé d'un long style glabre  dans le bouton la corolle, étroitement fermée, laisse poindre très apparemment le style  fruits inconnus  le spécimen type renferme une seule graine fusiforme non carénée, de 2 cm long, 0,6 large, 0,6 épaisseur, à cicatrice oblongue coupant toute la face ventrale, à bords crénelés"
    text = st.text_area("Entrer du texte ici",example_text)
    HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""
    
    if text:
        doc = nlp(text.lower())
        
        organes = {}
        org = ""
        org_count = 0
        desc_count = 0
        labels = []
        if doc.ents:
            for ent in doc.ents:
                labels.append(ent.label_)
                if ent.label_ == 'ORGANE':
                    org = ent.text
                    organes[org] = []  
                    org_count = org_count + 1
                else:
                    if ent.text and org:
                        organes[org].append(ent.text)
                        desc_count = desc_count + 1
            def vue_ner_output(ent): 
                main_org_dict = {}
                main_dict = {}
                for ent in doc.ents:
                    if ent.label_ == 'ORGANE':
                        org = ent.text
                        main_org_dict[org] = [] 
                    else:
                        if ent.text and org:
                            main_org_dict[org].append(ent.text)
                            main_dict[ent.text] = ent.label_
                
                dict_out = {}
                for i in main_org_dict.keys():
                    dict_out[i] = {}
                    for j in main_org_dict[i]:
                        row_dict = {}
                        dict_out[i][j]= main_dict[j]
                dict_out = {}
                for i in main_org_dict.keys():
                    dict_out[i] = {}
                    for j in main_org_dict[i]:
                        row_dict = {}
                        dict_out[i][j]= main_dict[j]

                

                return dict_out, main_org_dict, main_dict

            
            def vue_dataframe(main_org_dict, main_dict):
                # create dataframe
                dict_types={}
                dict_types['ORGANE'] = list(main_org_dict.keys())
                for l in labels:
                    if l != 'ORGANE':
                        dict_types[l] = []
                        for i in main_org_dict.keys():
                            row = []
                            for j in main_org_dict[i]:
                                if main_dict[j] == l:
                                    row.append(j)
                                else:
                                    row.append("-")
                            row = [e for e in row if e != "-"]
                            dict_types[l].append(", ".join(row))

                df_fined = pd.DataFrame.from_dict(dict_types)
                return df_fined
        if model_choice == 'Modèle v4 (fine-grained)' or model_choice == 'Modèle v4 (fine-grained updated)':
            labels = list(set(labels))
            

            if output_format == 'Highlighted':
                with st.sidebar:
                    named_entities_choice = st.multiselect('Entités nommées', labels, labels)
                colors = {
                    'ORGANE': "#cdcd00", 
                    "DESCRIPTEUR": "#85C1E9",
                    "FORME": "#60d394",
                    "MESURE": "#b1b6a6",
                    "STRUCTURE": "#e0aaff",
                    "DISPOSITION": "#fb8b24",
                    "COULEUR": "#ddb892",
                    "SURFACE": "#99582a",
                    "POSITION": "#9a031e",
                    "DEVELOPPEMENT": "#ff7d00"}

                # options = {"ents": ['ORGANE', 'DESCRIPTEUR', 'FORME', 'MESURE', 'STRUCTURE', 'DISPOSITION', 'COULEUR', 'SURFACE', 'POSITION', 'DEVELOPPEMENT'], "colors": colors}

                count_str = str(org_count)+" ORGANE et "+str(desc_count)+" DESCRIPTEUR."
                st.info(count_str)
                
                with st.expander("Affichage NER"):
                    options = {
                        "ents": named_entities_choice, 
                        "colors": colors
                        }        

                    html = displacy.render(doc,style="ent", options=options)
                    html = html.replace("\n\n","\n")  
                    st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)
            elif output_format == 'Vue dataframe':
                
                # ORGANIZE DATA IN DICT
                dict_out, main_org_dict, main_dict = vue_ner_output(doc.ents)
                # TO DATAFRAME
                df_fined = vue_dataframe(main_org_dict, main_dict)
                with st.expander("Vue dataframe"):
                    st.table(df_fined)

            elif output_format == 'Vue dictionnaire':
                # ORGANIZE DATA IN DICT
                # st.markdown("""
                # ### Vue dictionnaire
                # """)
                with st.expander("Vue dictionnaire"):
                    dict_out, main_org_dict, main_dict = vue_ner_output(doc.ents)
                    st.write(dict_out)
        else:

            if output_format == 'Highlighted':
                colors = {'ORGANE': "#cdcd00", "DESCRIPTEUR": "#85C1E9"}
                options = {"ents": ['ORGANE', 'DESCRIPTEUR'], "colors": colors}

                count_str = str(org_count)+" ORGANE et "+str(desc_count)+" DESCRIPTEUR."
                st.info(count_str)

                html = displacy.render(doc,style="ent", options=options)
                html = html.replace("\n\n","\n")
                with st.expander("Affichage NER"):
                    st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)
            
            elif output_format == 'Vue dataframe':
                st.markdown("""
                    
                    Chaque terme `DESCRIPTEUR` est associé au terme `ORGANE` qu'il précède.
                """)
                
                if doc.ents:
                    for o in organes.keys():
                        organes[o] = ", ".join(organes[o])

                    df_out = pd.DataFrame(organes.items(), columns=['ORGANE', 'DESCRIPTEUR'])
                    with st.expander("Vue dataframe"):
                        st.table(df_out)

                

        