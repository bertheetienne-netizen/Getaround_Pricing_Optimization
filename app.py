import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Getaround Analysis", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_excel("get_around_delay_analysis.xlsx")
    # Conserver les NaN originaux pour les calculs de lignes consécutives
    return df

df = load_data()

st.title("Getaround Analysis")
st.markdown("""
    Cette application aide à décider du **seuil de sécurité** (delay threshold) à appliquer entre deux locations 
    pour éviter les retards, tout en minimisant la perte de revenus.
""")

# SECTION 1
st.header("1. État des lieux de la flotte")
col1, col2, col3 = st.columns(3)

with col1:
    late_rate = (df['delay_at_checkout_in_minutes'] > 0).mean()
    st.metric("Taux de retard global", f"{late_rate:.1%}")

with col2:
    df_cons = df[df['previous_ended_rental_id'].notna()].copy()
    # retard ET ce retard est supérieur au battement prévu
    df_cons['is_friction'] = df_cons['delay_at_checkout_in_minutes'] > df_cons['time_delta_with_previous_rental_in_minutes']
    friction_rate = df_cons['is_friction'].mean()
    st.metric("Taux de friction réel", f"{friction_rate:.1%}", help="Cas où le retard a empiété sur la location suivante")

with col3:
    mobile_median = df[df['checkin_type'] == 'mobile']['delay_at_checkout_in_minutes'].median()
    st.metric("Retard médian (mobile)", f"{mobile_median:.0f} min")

# SECTION 2
st.header("2. Simulation d'impact business")

threshold = st.select_slider(
    "Choisissez un seuil de sécurité (en min) :",
    options=[0, 30, 60, 120, 180, 240, 300, 360, 480, 600],
    value=120
)

# Financement impacté : toutes les locations consécutives dont le battement initial était inférieur au nouveau seuil
total_rentals = len(df)
rentals_blocked = df_cons[df_cons['time_delta_with_previous_rental_in_minutes'] < threshold]
loss_count = len(rentals_blocked)
loss_pct = loss_count / total_rentals

# Frictions résolues : parmi les locations bloquées, combien étaient de vraies frictions ?
frictions_solved = rentals_blocked[rentals_blocked['is_friction'] == True]
solved_count = len(frictions_solved)

col_a, col_b = st.columns(2)

with col_a:
    st.error(f"Risque : **{loss_count}** locations seraient bloquées.")
    st.error(f"Perte potentielle : **{loss_pct:.2%}** des transactions de la plateforme.")

with col_b:
    st.success(f"**{solved_count}** cas de frictions clients résolus.")
    if loss_count > 0:
        efficiency = (solved_count / loss_count)
        st.success(f"Efficacité du ciblage : {efficiency:.1%} des blocages ont évité une vraie crise.")
    else:
        st.success("Efficacité du ciblage : 100%")

# SECTION 3
st.header("3. Distribution des retards par typologie")
df_late = df[df['delay_at_checkout_in_minutes'] > 0]
fig = px.box(df_late, 
             x='checkin_type', 
             y='delay_at_checkout_in_minutes',
             color='checkin_type',
             title="Distribution des retards au Checkout (Échelle Logarithmique)",
             log_y=True)
st.plotly_chart(fig, use_container_width=True)