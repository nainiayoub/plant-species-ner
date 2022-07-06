import streamlit as st
import spacy
from spacy import displacy
st.set_page_config(layout="wide")
nlp = spacy.load('./ner-species-model-recent')
html_temp = """
                <div style="background-color:{};padding:1px">
                
                </div>
                """

st.markdown("""
## Un modèle NER pour l'extraction des espèces de plantes
""")
st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)

example_text = "Oxera subverticillata est une liane robuste de forêt dense humide, largement répartie du centre au nord de la Grande Terre. Espèce assez commune avec une zone d'occurrence (EOO) de 3651 km² et une zone d'occupation de 100 km², O. subverticillata est évalué en Préoccupation Mineure (LC)."
text = st.text_area("Entrer du texte ici",example_text)
HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""
if text:
    doc = nlp(text)
    html = displacy.render(doc,style="ent")
    html = html.replace("\n\n","\n")
    st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)

