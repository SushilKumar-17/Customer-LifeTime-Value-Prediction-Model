# Set page config - MUST BE FIRST COMMAND
import streamlit as st
st.set_page_config(
    page_title="Customer Lifetime Value Predictor", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Other imports
import os
import pandas as pd
import numpy as np
import joblib
import json
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime, timedelta

# Load model and selected features
@st.cache_resource
def load_model_and_features():
    base_path = os.path.dirname(__file__)  # Gets the directory where app.py is
    model_path = os.path.join(base_path, "xgb_clv_model.pkl")
    features_path = os.path.join(base_path, "selected_features.json")

    model = joblib.load(model_path)
    with open(features_path, "r") as f:
        selected_features = json.load(f)
    return model, selected_features

model, selected_features = load_model_and_features()

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        text-align: center;
        color: white;
    }
    .prediction-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        color: white;
    }
    .metric-box {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'predictions_history' not in st.session_state:
    st.session_state.predictions_history = []
if 'current_prediction' not in st.session_state:
    st.session_state.current_prediction = None

# Header
st.markdown("""
<div class="main-header">
    <h1>Customer Lifetime Value Predictor</h1>
    <p>Predict 12-month CLV using machine learning</p>
</div>
""", unsafe_allow_html=True)

# Sidebar inputs
st.sidebar.header("Customer Information")

# Input fields
st.sidebar.markdown("**Financial Data**")
total_spend = st.sidebar.number_input("Total Spend (₹)", min_value=0.0, value=1000.0, step=100.0)
purchase_freq = st.sidebar.number_input("Purchase Frequency", min_value=1.0, value=10.0, step=1.0)

st.sidebar.markdown("**Time-based Data**")
tenure = st.sidebar.slider("Tenure (days)", min_value=1, max_value=365, value=180)
avg_gap = st.sidebar.slider("Average Purchase Gap (days)", min_value=1, max_value=200, value=15)
recency = st.sidebar.slider("Days Since Last Purchase", min_value=1, max_value=365, value=30)

st.sidebar.markdown("**Behavioral Data**")
order_habit = st.sidebar.slider("Order Habit Score (0-100)", min_value=0.0, max_value=100.0, value=50.0)
engagement_score = st.sidebar.slider("Engagement Score (0-1)", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
return_rate = st.sidebar.slider("Return Rate (0-1)", min_value=0.0, max_value=1.0, value=0.1, step=0.01)

# Calculate derived features
def calculate_features(total_spend, purchase_freq, tenure, avg_gap, recency, order_habit, engagement_score, return_rate):
    return {
        "TotalSpend": total_spend,
        "OrderHabit": order_habit,
        "Tenure": tenure,
        "SpendPerOrder": total_spend / purchase_freq,
        "SpendRate": total_spend / tenure,
        "EngagementScore": engagement_score,
        "ReturnImpact": return_rate * total_spend,
        "RecencySpendRatio": total_spend / (recency + 1),
        "RecentEngagement": engagement_score / (recency + 1),
        "GapEngagement": engagement_score / (avg_gap + 1),
        "GapHabitScore": order_habit / (avg_gap + 1)
    }

# Main content with tabs
tab1, tab2, tab3 = st.tabs(["Prediction", "Customer Analysis", "History"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Calculated Features")
        input_data = calculate_features(total_spend, purchase_freq, tenure, avg_gap, recency, order_habit, engagement_score, return_rate)
        
        # Display key metrics
        col1a, col1b, col1c = st.columns(3)
        with col1a:
            st.metric("Spend per Order", f"₹{input_data['SpendPerOrder']:.2f}")
            st.metric("Return Impact", f"₹{input_data['ReturnImpact']:.2f}")
        with col1b:
            st.metric("Spend Rate", f"₹{input_data['SpendRate']:.2f}/day")
            st.metric("Recent Engagement", f"{input_data['RecentEngagement']:.3f}")
        with col1c:
            st.metric("Recency Spend Ratio", f"{input_data['RecencySpendRatio']:.2f}")
            st.metric("Gap Engagement", f"{input_data['GapEngagement']:.3f}")
        
        # Prediction button
        if st.button("Predict CLV"):
            with st.spinner("Calculating CLV..."):
                time.sleep(0.5)
                
                X_input = pd.DataFrame([input_data])
                prediction = model.predict(X_input)[0]
                
                # Store prediction
                st.session_state.predictions_history.append({
                    'timestamp': datetime.now(),
                    'prediction': prediction,
                    'total_spend': total_spend,
                    'engagement_score': engagement_score,
                    'recency': recency
                })
                
                st.session_state.current_prediction = prediction
                
                # Display prediction
                st.markdown(f"""
                <div class="prediction-box">
                    <h2>Predicted CLV</h2>
                    <h1>₹{prediction:,.2f}</h1>
                    <p>Expected value for next 12 months</p>
                </div>
                """, unsafe_allow_html=True)
                
                # CLV category
                if prediction < 1000:
                    st.warning("Low CLV - Consider retention strategies")
                elif prediction < 5000:
                    st.info("Medium CLV - Good growth potential")
                else:
                    st.success("High CLV - Excellent customer!")
    
    with col2:
        st.subheader("Customer Status")
        st.markdown("*Risk Assessment: Likelihood of customer churn or reduced spending*")
        
        # Risk assessment logic (separate from CLV value)
        risk_score = 0
        risk_factors = []
        
        # Risk factor logic (enhanced sensitivity)
        if recency > 45:
            risk_factors.append("Customer hasn't purchased recently (high recency)")
            risk_score += 25
        if engagement_score < 0.4:
            risk_factors.append("Low engagement score")
            risk_score += 20
        if return_rate > 0.15:
            risk_factors.append("Above-average return rate")
            risk_score += 20
        if avg_gap > 30:
            risk_factors.append("Inconsistent purchase pattern")
            risk_score += 15

        # Determine customer risk level
        if risk_score >= 60:
            st.error(f"High Risk Customer (Score: {risk_score})")
            st.write("*Significant risk of churn or reduced future value*")
        elif risk_score >= 30:
            st.warning(f"Medium Risk Customer (Score: {risk_score})")
            st.write("*Monitor behavior — potential to shift segments*")
        else:
            st.success(f"Low Risk Customer (Score: {risk_score})")
            st.write("*Customer shows strong and consistent engagement*")

        # Show risk breakdown
        if risk_factors:
            st.write("**Contributing Risk Factors:**")
            for factor in risk_factors:
                st.write(f"• {factor}")

        # Customer lifecycle stage
        st.markdown("---")
        st.write("**Customer Lifecycle Stage:**")
        st.markdown("*Estimated from customer tenure*")
        if tenure < 60:
            st.write("**New Customer** (< 2 months)")
        elif tenure < 150:
            st.write("**Early Stage Customer** (2–5 months)")
        elif tenure < 300:
            st.write("**Established Customer** (5–10 months)")
        else:
            st.write("**Loyal Customer** (10+ months)")


with tab2:
    st.subheader("Feature Analysis")
    
    if st.session_state.current_prediction:
        # Simple bar chart of features
        fig = px.bar(
            x=list(input_data.keys()), 
            y=list(input_data.values()),
            title="Feature Values Used in Prediction",
            labels={'x': 'Features', 'y': 'Values'}
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Business recommendations
        st.subheader("Recommendations")
        recommendations = []
        
        if engagement_score < 0.4:
            recommendations.append("Increase customer engagement through targeted campaigns")
        
        if recency > 45:
            recommendations.append("Launch win-back campaign for inactive customer")
        
        if return_rate > 0.15:
            recommendations.append("Review product quality to reduce returns")
        
        if total_spend / purchase_freq < 200:
            recommendations.append("Focus on upselling to increase order value")
        
        if avg_gap > 30:
            recommendations.append("Implement loyalty programs to increase purchase frequency")
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                st.write(f"{i}. {rec}")
        else:
            st.success("Customer shows healthy engagement patterns!")
    else:
        st.info("Make a prediction to see analysis")

with tab3:
    st.subheader("Prediction History")
    
    if st.session_state.predictions_history:
        # Convert to DataFrame
        history_df = pd.DataFrame(st.session_state.predictions_history)
        
        # Summary statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Predictions", len(history_df))
        with col2:
            st.metric("Average CLV", f"₹{history_df['prediction'].mean():.2f}")
        with col3:
            st.metric("Highest CLV", f"₹{history_df['prediction'].max():.2f}")
        with col4:
            st.metric("Lowest CLV", f"₹{history_df['prediction'].min():.2f}")
        
        # Trend chart
        if len(history_df) > 1:
            fig = px.line(
                history_df, 
                x='timestamp', 
                y='prediction',
                title='CLV Predictions Over Time',
                markers=True
            )
            fig.update_layout(xaxis_title="Time", yaxis_title="Predicted CLV (₹)")
            st.plotly_chart(fig, use_container_width=True)
        
        # Recent predictions table
        st.subheader("Recent Predictions")
        recent_df = history_df.tail(10).copy()
        recent_df['timestamp'] = recent_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        recent_df['prediction'] = recent_df['prediction'].apply(lambda x: f"₹{x:,.2f}")
        st.dataframe(recent_df[['timestamp', 'prediction', 'total_spend', 'engagement_score', 'recency']], use_container_width=True)
        
        # Export option
        if st.button("Export History"):
            csv = history_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"clv_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    else:
        st.info("No predictions yet. Make your first prediction to see history!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    <p><strong>Customer Lifetime Value Predictor</strong></p>
    <p>Built by: Sushil Kumar Patra | Data Science Project</p>
</div>
            

""", unsafe_allow_html=True)

