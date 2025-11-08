hello updated changes or about new files here in written format


# ♿ Inclusive Job Recommendation System (India-focused)

### 🎯 Overview
This project uses Machine Learning and NLP to recommend jobs for people with disabilities in India.  
It combines skill-based matching with accessibility filtering to promote inclusive hiring.

---

### ⚙️ How It Works
1. Job data (from LinkedIn dataset) is cleaned and filtered for Indian postings.  
2. SentenceTransformer converts each job description into embeddings.  
3. A user enters their skills and disability type.  
4. The system computes semantic similarity and accessibility scores.  
5. Streamlit app displays top recommended jobs.

---

### 🧩 Technologies Used
- **Python**
- **Pandas, NumPy**
- **SentenceTransformer (all-MiniLM-L6-v2)**
- **Scikit-learn**
- **Streamlit**

---

### 🚀 How to Run
1. Clone or download this folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
