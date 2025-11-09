import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ==============================
# ✅ PAGE CONFIG
# ==============================
st.set_page_config(page_title="Saarthi Inclusive Job Recommender", page_icon="🧭", layout="wide")

# ==============================
# ✅ LOAD DATA AND MODEL
# ==============================
@st.cache_resource
def load_model_and_data():
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    df = pd.read_csv(r"C:/Users/suraj/Desktop/saarthiii/data/combined_dataset.csv")
    embeddings = np.load(r"C:/Users/suraj/Desktop/saarthiii/models/job_embeddings.npy")
    return model, df, embeddings

model, df, job_embeddings = load_model_and_data()
st.sidebar.success("✅ Model & dataset loaded successfully!")

# ==============================
# ✅ HELPER FUNCTION
# ==============================
def recommend_jobs(user_input, disability_type=None, top_n=5):
    # Encode user input
    user_embedding = model.encode([user_input], convert_to_tensor=False)
    user_embedding = np.array(user_embedding).reshape(1, -1)

    # Compute cosine similarity
    similarity_scores = cosine_similarity(user_embedding, job_embeddings)[0]
    df["similarity_score"] = similarity_scores

    # Optional: filter for disability-friendly jobs
    if disability_type and disability_type.lower() != "none":
        df_filtered = df[df["suitable_for_disability"].str.contains(disability_type, case=False, na=False)]
    else:
        df_filtered = df.copy()

    # Sort by similarity score
    recommendations = df_filtered.sort_values(by="similarity_score", ascending=False).head(top_n)
    return recommendations

# ==============================
# ✅ STREAMLIT FRONTEND
# ==============================
st.title("🧭 Saarthi: Inclusive Job Recommender System")
st.markdown("Find jobs that match your skills and accessibility needs. Empowering persons with disabilities (PWDs) through inclusive opportunities. 💪")

with st.form("job_form"):
    user_input = st.text_area("💼 Enter your skills or job interests:", "Python, SQL, Excel, Data Analysis")
    disability_type = st.selectbox(
        "♿ Select your disability type:",
        ["none", "visual_impairment", "hearing_impairment", "speech_impairment", "mobility_impairment"]
    )
    top_n = st.slider("🔢 Number of job recommendations:", 3, 15, 5)
    submitted = st.form_submit_button("Find Jobs")

if submitted:
    with st.spinner("🔍 Finding best matching jobs..."):
        recommendations = recommend_jobs(user_input, disability_type, top_n)
    
    st.success(f"✅ Found {len(recommendations)} recommended jobs for your profile!")

    st.dataframe(
        recommendations[["job_title", "company_name", "category", "similarity_score", "suitable_for_disability"]]
    )

    # Show average similarity score
    avg_score = recommendations["similarity_score"].mean()
    st.metric("Average Similarity Score", f"{avg_score:.2f}")

# ==============================
# ✅ FOOTER
# ==============================
st.caption("Built with ❤️ using SentenceTransformer, Streamlit, and real job datasets. (Team Saarthi)")
