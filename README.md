# Real Estate Price Prediction and Investment Analyzer

## Major College Project

**Submitted by: Parth Makwana**

An academic AI/ML and Streamlit platform that estimates property values, analyzes locality-level market factors, scores potential deals, projects investment returns, compares properties, and visualizes property intelligence on a map.

### Major modules
1. Market dashboard
2. AI price prediction
3. Locality intelligence
4. Investment analyzer
5. Deal scorer
6. Property comparison
7. Map intelligence with heatmap and circle-drawing tools
8. Model evaluation

### ML
- Gradient Boosting Regressor
- Random Forest Regressor
- One-hot encoding for categorical variables
- Median imputation for missing numeric values
- Train/test evaluation with MAE, RMSE and R²

### Data
The included data is **synthetic demonstration data** for academic development and testing. Replace it with legally obtained, documented real-estate data before making real-world claims.

### Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/train_models.py
streamlit run app.py
```

Streamlit's documented workflow uses `streamlit run app.py`, and deployment services expect project dependencies to be listed in `requirements.txt`.

### GitHub / Colab
GitHub Repository: `PASTE_YOUR_GITHUB_REPOSITORY_LINK_HERE`
Colab Notebook: `PASTE_YOUR_GOOGLE_COLAB_LINK_HERE`

### Academic note
This system is a decision-support prototype, not a property valuation guarantee or financial advice tool.
