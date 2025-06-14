import streamlit as st
import time
from model.drug_processor import load_drug_data, get_drug_categories, get_classification_fields
from model.compare import compare_drugs
from model.explain import generate_explanation

# ✅ Streamlit config - must be first
st.set_page_config(page_title="DrugCompare", layout="centered")

# ✅ Load and cache dataset
@st.cache_data
def get_data():
    df = load_drug_data()
    categories = get_drug_categories(df)
    fields = get_classification_fields(df)
    return df, categories, fields

df, categories, fields = get_data()

# ✅ UI Setup
st.title("💊 DrugCompare – Smart Drug Comparison Tool")
st.markdown(
    "Select a drug category, choose two medications, and compare their medical properties."
)

# 🔍 Sidebar Inputs
st.sidebar.header("🔎 Filter Drugs")
selected_category = st.sidebar.selectbox("Select Category", sorted(categories))

filtered_df = df[df["groups"].str.contains(selected_category, case=False, na=False)]
# Only show drugs with at least one populated field in required fields
valid_drugs = filtered_df.dropna(subset=fields, how='all')
drug_options = sorted(valid_drugs["name"].dropna().unique())

drug1 = st.sidebar.selectbox("Choose First Drug", drug_options, key="drug1")
drug2 = st.sidebar.selectbox("Choose Second Drug", drug_options, key="drug2")

if drug1 == drug2:
    st.sidebar.warning("Please select two different drugs to compare.")
    st.stop()

generate_llm = st.sidebar.checkbox("🧠 Generate LLM Explanation", value=True)

# 🧪 Comparison Output
if st.sidebar.button("Compare"):
    with st.spinner("🔄 Comparing drugs..."):
        time.sleep(0.2)
        result = compare_drugs(df, drug1, drug2, fields)

    st.success("✅ Comparison complete!")
    st.header(f"🧪 {drug1} vs {drug2}")

    for field, values in result.items():
        st.subheader(field.replace("_", " ").title())
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**{drug1}:**\n\n{values['drug1'] or '_No data available_'}")
        with col2:
            st.markdown(f"**{drug2}:**\n\n{values['drug2'] or '_No data available_'}")

    result = compare_drugs(df, drug1, drug2, fields)

    if generate_llm:
        st.divider()
        st.subheader("📘 AI-Powered Summary")
        explanation = generate_explanation(drug1, drug2, result)
        st.markdown(explanation)
