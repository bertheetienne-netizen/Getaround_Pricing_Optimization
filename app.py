import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(page_title="Getaround Analysis", layout="wide")

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_excel("get_around_delay_analysis.xlsx")
    df['delay_at_checkout_in_minutes'] = df['delay_at_checkout_in_minutes'].fillna(0)
    return df

df = load_data()

st.title("Getaround Analysis")
st.markdown("""
    Cette application aide à décider du **seuil de sécurité** (delay threshold) à appliquer entre deux locations 
    pour éviter les retards, tout en minimisant la perte de revenus.
""")

# SECTION 1 : CHIFFRES CLÉS
st.header("1. État des lieux de la flotte")
col1, col2, col3 = st.columns(3)

with col1:
    late_rate = (df['delay_at_checkout_in_minutes'] > 0).mean()
    st.metric("Taux de retard global", f"{late_rate:.1%}")

with col2:
    # Calcul de la friction sur les locations consécutives
    df_cons = df[df['previous_ended_rental_id'].notna()]
    friction = (df_cons['delay_at_checkout_in_minutes'] > df_cons['time_delta_with_previous_rental_in_minutes']).mean()
    st.metric("Taux de friction", f"{friction:.1%}", help="Cas où le retard impacte le locataire suivant")

with col3:
    st.metric("Retard médian (mobile)", "14 min")

# SECTION 2 : IMPACT DU SEUIL
st.header("2. Simulation d'impact business")

# Slider seuil
threshold = st.select_slider(
    "Choisissez un seuil de sécurité (en min) :",
    options=[0, 30, 60, 120, 180, 240, 300, 360, 480, 600],
    value=120
)

# Calcul de l'impact
impacted_rentals = df_cons[df_cons['time_delta_with_previous_rental_in_minutes'] < threshold]
loss_count = len(impacted_rentals)
loss_pct = loss_count / len(df)

col_a, col_b = st.columns(2)

with col_a:
    st.error(f"Risque : **{loss_count}** locations seraient annulées/bloquées")
    st.error(f"Représente une perte potentielle de **{loss_pct:.2%}** du CA total")

with col_b:
    solved_cases = impacted_rentals[impacted_rentals['delay_at_checkout_in_minutes'] > impacted_rentals['time_delta_with_previous_rental_in_minutes']]
    st.success(f"**{len(solved_cases)}** cas de friction seraient résolus.")
    st.success(f"Efficacité : {(len(solved_cases)/len(impacted_rentals)):.1%} de blocages utiles.")

# SECTION 3 : VISUALISATION
st.header("3. Comparaison connect vs mobile")

fig = px.box(df[df['delay_at_checkout_in_minutes'] > 0], 
             x='checkin_type', 
             y='delay_at_checkout_in_minutes',
             color='checkin_type',
             points="all",
             title="Distribution des retards (log scale)",
             log_y=True)
st.plotly_chart(fig, use_container_width=True)

st.info("**Conseil Stratégique :** Au vu des données, les voitures 'connect' sont beaucoup plus ponctuelles. Il pourrait être judicieux de n'appliquer le seuil qu'aux voitures en check-in 'mobile'.")