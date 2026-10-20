import streamlit as st
import requests

# ============== CONFIGURATION DE LA PAGE ==============
st.set_page_config(
    page_title="Prédiction Churn Client",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = "http://127.0.0.1:8000/predict"

# ============== CSS PERSONNALISÉ ==============
st.markdown("""
<style>
    /* Fond général */
    .main {
        background-color: #f5f7fa;
    }

    /* Titre principal */
    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #6b7280;
        margin-top: 0;
        margin-bottom: 1.5rem;
    }

    /* Cartes de section */
    .section-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
    }

    /* Bouton principal */
    div.stButton > button, button[kind="formSubmit"] {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        border: none;
        width: 100%;
        transition: 0.2s;
    }
    div.stButton > button:hover, button[kind="formSubmit"]:hover {
        background-color: #1d4ed8;
    }

    /* Cartes de résultat */
    .result-card-danger {
        background-color: #fef2f2;
        border-left: 6px solid #dc2626;
        padding: 1.3rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    .result-card-success {
        background-color: #f0fdf4;
        border-left: 6px solid #16a34a;
        padding: 1.3rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    .result-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    /* Metric cards sidebar */
    .metric-box {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }

    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============== SIDEBAR ==============
with st.sidebar:
    st.markdown("## 🏦 Churn Predictor")
    st.markdown("Application de prédiction de résiliation client, basée sur un modèle **Random Forest** entraîné sur les données bancaires.")
    st.markdown("---")
    st.markdown("### ℹ️ À propos")
    st.markdown(
        "- **Modèle** : RandomForestClassifier\n"
        "- **Données** : Churn_Modelling.csv\n"
        "- **API** : FastAPI `/predict`\n"
    )
    st.markdown("---")
    api_status = "🟢 En ligne" if True else "🔴 Hors ligne"
    try:
        requests.get("http://127.0.0.1:8000/", timeout=2)
        st.success("API connectée")
    except Exception:
        st.error("API injoignable")

# ============== EN-TÊTE ==============
st.markdown('<p class="main-title">📊 Prédiction de Churn Client</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Renseignez le profil du client pour estimer sa probabilité de résiliation</p>', unsafe_allow_html=True)

# ============== FORMULAIRE ==============
with st.container():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    with st.form("formulaire_prediction"):
        tab1, tab2 = st.tabs(["👤 Profil client", "💳 Informations bancaires"])

        with tab1:
            c1, c2 = st.columns(2)
            with c1:
                geography = st.selectbox("🌍 Pays", ["France", "Germany", "Spain"])
                age = st.slider("🎂 Âge", 18, 100, 40)
            with c2:
                gender = st.selectbox("⚧ Genre", ["Male", "Female"])
                tenure = st.slider("📅 Ancienneté (années)", 0, 20, 3)

        with tab2:
            c3, c4 = st.columns(2)
            with c3:
                credit_score = st.slider("💯 Score de crédit", 300, 900, 600)
                balance = st.number_input("💰 Solde du compte (€)", min_value=0.0, value=60000.0, step=1000.0)
                num_products = st.selectbox("📦 Nombre de produits souscrits", [1, 2, 3, 4], index=1)
            with c4:
                estimated_salary = st.number_input("💵 Salaire estimé (€)", min_value=0.0, value=50000.0, step=1000.0)
                has_cr_card = st.radio("💳 Possède une carte de crédit ?", ["Oui", "Non"], horizontal=True)
                is_active = st.radio("✅ Membre actif ?", ["Oui", "Non"], horizontal=True)

        st.markdown("<br>", unsafe_allow_html=True)
        submit = st.form_submit_button("🔮 Lancer la prédiction")

    st.markdown('</div>', unsafe_allow_html=True)

# ============== APPEL API & RÉSULTAT ==============
if submit:
    payload = {
        "CreditScore": int(credit_score),
        "Geography": geography,
        "Gender": gender,
        "Age": int(age),
        "Tenure": int(tenure),
        "Balance": float(balance),
        "NumOfProducts": int(num_products),
        "HasCrCard": 1 if has_cr_card == "Oui" else 0,
        "IsActiveMember": 1 if is_active == "Oui" else 0,
        "EstimatedSalary": float(estimated_salary),
    }

    try:
        with st.spinner("🔄 Analyse du profil en cours..."):
            response = requests.post(API_URL, json=payload, timeout=10)

        if response.status_code == 200:
            result = response.json()
            churn = result["churn"]
            proba = result["probabilite_churn"]

            if churn:
                st.markdown(f"""
                <div class="result-card-danger">
                    <p class="result-title">⚠️ Risque de résiliation élevé</p>
                    <p>Ce client présente une probabilité de churn de <b>{proba*100:.1f}%</b>.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-card-success">
                    <p class="result-title">✅ Client fidèle</p>
                    <p>Probabilité de résiliation estimée : <b>{proba*100:.1f}%</b>.</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("#### Probabilité de churn")
            st.progress(proba)

            m1, m2, m3 = st.columns(3)
            m1.metric("Probabilité de Churn", f"{proba*100:.1f} %")
            m2.metric("Probabilité de rétention", f"{(1-proba)*100:.1f} %")
            m3.metric("Verdict", "Churn" if churn else "Fidèle", delta=None)

        else:
            st.error(f"❌ Erreur API ({response.status_code}) : {response.json().get('detail', 'Erreur inconnue')}")

    except requests.exceptions.ConnectionError:
        st.error("❌ Impossible de contacter l'API. Vérifiez qu'elle tourne sur http://127.0.0.1:8000.")
    except Exception as e:
        st.error(f"Erreur inattendue : {e}")

# ============== FOOTER ==============
st.markdown("---")
st.caption("🔗 API consommée : `POST /predict` — Modèle entraîné sur `Churn_Modelling.csv` | UP ASI – Équipe MLOps")
# import streamlit as st
# import requests

# # URL de l'API FastAPI (ajustez si l'API tourne sur une autre machine/port)
# API_URL = "http://127.0.0.1:8000/predict"

# st.set_page_config(page_title="Prédiction Churn", page_icon="📊", layout="centered")

# st.title("📊 Prédiction de Churn Client")
# st.write("Remplissez le formulaire ci-dessous pour prédire si un client va résilier (churn).")

# with st.form("formulaire_prediction"):
#     col1, col2 = st.columns(2)

#     with col1:
#         credit_score = st.number_input("Score de crédit (CreditScore)", min_value=300, max_value=900, value=600)
#         geography = st.selectbox("Pays (Geography)", ["France", "Germany", "Spain"])
#         gender = st.selectbox("Genre (Gender)", ["Male", "Female"])
#         age = st.number_input("Âge (Age)", min_value=18, max_value=100, value=40)
#         tenure = st.number_input("Ancienneté en années (Tenure)", min_value=0, max_value=20, value=3)

#     with col2:
#         balance = st.number_input("Solde du compte (Balance)", min_value=0.0, value=60000.0, step=1000.0)
#         num_products = st.number_input("Nombre de produits (NumOfProducts)", min_value=1, max_value=4, value=2)
#         has_cr_card = st.selectbox("Possède une carte de crédit ?", ["Oui", "Non"])
#         is_active = st.selectbox("Membre actif ?", ["Oui", "Non"])
#         estimated_salary = st.number_input("Salaire estimé (EstimatedSalary)", min_value=0.0, value=50000.0, step=1000.0)

#     submit = st.form_submit_button("🔮 Lancer la prédiction")

# if submit:
#     payload = {
#         "CreditScore": int(credit_score),
#         "Geography": geography,
#         "Gender": gender,
#         "Age": int(age),
#         "Tenure": int(tenure),
#         "Balance": float(balance),
#         "NumOfProducts": int(num_products),
#         "HasCrCard": 1 if has_cr_card == "Oui" else 0,
#         "IsActiveMember": 1 if is_active == "Oui" else 0,
#         "EstimatedSalary": float(estimated_salary),
#     }

#     try:
#         with st.spinner("Prédiction en cours..."):
#             response = requests.post(API_URL, json=payload, timeout=10)

#         if response.status_code == 200:
#             result = response.json()
#             churn = result["churn"]
#             proba = result["probabilite_churn"]

#             st.subheader("Résultat")
#             if churn:
#                 st.error(f"⚠️ Ce client risque de résilier (Churn). Probabilité : {proba*100:.2f}%")
#             else:
#                 st.success(f"✅ Ce client va probablement rester. Probabilité de churn : {proba*100:.2f}%")

#             st.progress(proba)

#         else:
#             st.error(f"Erreur API ({response.status_code}) : {response.json().get('detail', 'Erreur inconnue')}")

#     except requests.exceptions.ConnectionError:
#         st.error("❌ Impossible de contacter l'API. Vérifiez qu'elle tourne bien sur http://127.0.0.1:8000.")
#     except Exception as e:
#         st.error(f"Erreur inattendue : {e}")

# st.markdown("---")
# st.caption("API FastAPI consommée : `/predict` — Modèle : RandomForestClassifier (Churn_Modelling.csv)")