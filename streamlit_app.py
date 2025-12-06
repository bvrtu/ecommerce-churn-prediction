"""
Streamlit web application for E-commerce Churn Prediction.
Provides a user-friendly interface for model inference.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.inference import ChurnPredictor
from src.config import MODELS_DIR, BUSINESS_RULES

# Page configuration
st.set_page_config(
    page_title="E-commerce Churn Prediction",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .high-risk {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
    }
    .medium-risk {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
    }
    .low-risk {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'predictor' not in st.session_state:
    try:
        st.session_state.predictor = ChurnPredictor()
        st.session_state.model_loaded = True
    except Exception as e:
        st.session_state.model_loaded = False
        st.session_state.model_error = str(e)


def main():
    """Main application function."""
    # Header
    st.markdown('<div class="main-header">📊 E-commerce Churn Prediction Dashboard</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Select Page",
            ["Single Prediction", "Batch Prediction", "Model Info"]
        )
        
        st.header("Business Rules")
        st.info(f"""
        **Churn Definition**: {BUSINESS_RULES['churn_definition']}
        
        **Retention Cost**: ${BUSINESS_RULES['retention_cost']}
        
        **Acquisition Cost**: ${BUSINESS_RULES['acquisition_cost']}
        
        **Min Precision**: {BUSINESS_RULES['min_precision']}
        
        **Min Recall**: {BUSINESS_RULES['min_recall']}
        """)
    
    # Check if model is loaded
    if not st.session_state.model_loaded:
        st.error(f"❌ Model could not be loaded: {st.session_state.model_error}")
        st.info("Please ensure the model is trained first by running: `python src/pipeline.py`")
        return
    
    # Page routing
    if page == "Single Prediction":
        single_prediction_page()
    elif page == "Batch Prediction":
        batch_prediction_page()
    elif page == "Model Info":
        model_info_page()


def single_prediction_page():
    """Single customer prediction page."""
    st.header("🔮 Single Customer Prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Customer Demographics")
        
        customer_id = st.text_input("Customer ID", value="7590-VHVEG")
        gender = st.selectbox("Gender", ["Male", "Female"])
        senior_citizen = st.selectbox("Senior Citizen", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        partner = st.selectbox("Partner", ["Yes", "No"])
        dependents = st.selectbox("Dependents", ["Yes", "No"])
        tenure = st.number_input("Tenure (months)", min_value=0, max_value=100, value=12)
    
    with col2:
        st.subheader("Services & Contract")
        
        phone_service = st.selectbox("Phone Service", ["Yes", "No"])
        multiple_lines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
        internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        online_security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
        online_backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
        device_protection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
        tech_support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
        streaming_tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
        streaming_movies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
        paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
        payment_method = st.selectbox("Payment Method", [
            "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"
        ])
        monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, value=50.0, step=0.01)
        total_charges = st.number_input("Total Charges ($)", min_value=0.0, value=500.0, step=0.01)
    
    # Prediction button
    if st.button("🔍 Predict Churn", type="primary", use_container_width=True):
        customer_data = {
            'customerID': customer_id,
            'gender': gender,
            'SeniorCitizen': senior_citizen,
            'Partner': partner,
            'Dependents': dependents,
            'tenure': tenure,
            'PhoneService': phone_service,
            'MultipleLines': multiple_lines,
            'InternetService': internet_service,
            'OnlineSecurity': online_security,
            'OnlineBackup': online_backup,
            'DeviceProtection': device_protection,
            'TechSupport': tech_support,
            'StreamingTV': streaming_tv,
            'StreamingMovies': streaming_movies,
            'Contract': contract,
            'PaperlessBilling': paperless_billing,
            'PaymentMethod': payment_method,
            'MonthlyCharges': monthly_charges,
            'TotalCharges': total_charges,
        }
        
        try:
            result = st.session_state.predictor.predict(customer_data)
            
            # Display results
            st.markdown("---")
            st.subheader("📊 Prediction Results")
            
            # Risk level styling
            risk_level = result['risk_level']
            risk_class = {
                'High': 'high-risk',
                'Medium': 'medium-risk',
                'Low': 'low-risk'
            }[risk_level]
            
            st.markdown(f'<div class="prediction-box {risk_class}">', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Churn Prediction", "Yes" if result['churn_prediction'] == 1 else "No")
            
            with col2:
                st.metric("Churn Probability", f"{result['churn_probability']:.2%}")
            
            with col3:
                st.metric("Risk Level", risk_level)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Probability visualization
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=result['churn_probability'] * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Churn Probability (%)"},
                delta={'reference': 50},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 40], 'color': "lightgreen"},
                        {'range': [40, 70], 'color': "yellow"},
                        {'range': [70, 100], 'color': "red"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 70
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # Business recommendation
            st.subheader("💡 Business Recommendation")
            if result['churn_probability'] > 0.7:
                st.warning(f"""
                **High Risk Customer** - Immediate action required!
                
                - Send personalized retention offer (${BUSINESS_RULES['retention_cost']})
                - Assign dedicated account manager
                - Schedule follow-up call within 24 hours
                - Offer exclusive discount or loyalty points
                """)
            elif result['churn_probability'] > 0.4:
                st.info(f"""
                **Medium Risk Customer** - Proactive engagement recommended
                
                - Send targeted email campaign
                - Offer relevant product recommendations
                - Invite to loyalty program if not already enrolled
                """)
            else:
                st.success(f"""
                **Low Risk Customer** - Maintain current engagement
                
                - Continue regular communication
                - Monitor for any behavior changes
                - Upsell/cross-sell opportunities
                """)
        
        except Exception as e:
            st.error(f"Error making prediction: {e}")


def batch_prediction_page():
    """Batch prediction page."""
    st.header("📦 Batch Prediction")
    
    st.info("Upload a CSV file with customer data or use the template below.")
    
    # Template download - Telco dataset format
    template_data = {
        'customerID': ['7590-VHVEG', '5575-GNVDE', '3668-QPYBK'],
        'gender': ['Female', 'Male', 'Male'],
        'SeniorCitizen': [0, 0, 0],
        'Partner': ['Yes', 'No', 'No'],
        'Dependents': ['No', 'No', 'No'],
        'tenure': [1, 34, 2],
        'PhoneService': ['No', 'Yes', 'Yes'],
        'MultipleLines': ['No phone service', 'No', 'No'],
        'InternetService': ['DSL', 'DSL', 'DSL'],
        'OnlineSecurity': ['No', 'Yes', 'Yes'],
        'OnlineBackup': ['Yes', 'No', 'Yes'],
        'DeviceProtection': ['No', 'Yes', 'No'],
        'TechSupport': ['No', 'No', 'No'],
        'StreamingTV': ['No', 'No', 'No'],
        'StreamingMovies': ['No', 'No', 'No'],
        'Contract': ['Month-to-month', 'One year', 'Month-to-month'],
        'PaperlessBilling': ['Yes', 'No', 'Yes'],
        'PaymentMethod': ['Electronic check', 'Mailed check', 'Mailed check'],
        'MonthlyCharges': [29.85, 56.95, 53.85],
        'TotalCharges': [29.85, 1889.5, 108.15],
    }
    template_df = pd.DataFrame(template_data)
    
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    with col2:
        st.download_button(
            "Download Template",
            template_df.to_csv(index=False),
            "template.csv",
            "text/csv"
        )
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.subheader("Uploaded Data Preview")
        st.dataframe(df.head())
        
        if st.button("🔍 Predict Churn for All Customers", type="primary"):
            try:
                results = st.session_state.predictor.predict_batch(df)
                results_df = pd.DataFrame(results)
                
                st.subheader("📊 Prediction Results")
                st.dataframe(results_df)
                
                # Summary statistics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Customers", len(results_df))
                with col2:
                    st.metric("High Risk", len(results_df[results_df['risk_level'] == 'High']))
                with col3:
                    st.metric("Medium Risk", len(results_df[results_df['risk_level'] == 'Medium']))
                with col4:
                    st.metric("Low Risk", len(results_df[results_df['risk_level'] == 'Low']))
                
                # Distribution chart
                fig = px.pie(
                    results_df,
                    names='risk_level',
                    title='Risk Level Distribution',
                    color='risk_level',
                    color_discrete_map={'High': 'red', 'Medium': 'orange', 'Low': 'green'}
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Download results
                csv = results_df.to_csv(index=False)
                st.download_button(
                    "Download Results",
                    csv,
                    "churn_predictions.csv",
                    "text/csv"
                )
            
            except Exception as e:
                st.error(f"Error processing batch prediction: {e}")


def model_info_page():
    """Model information page."""
    st.header("ℹ️ Model Information")
    
    st.subheader("Model Details")
    st.info("""
    **Model Type**: XGBoost Classifier
    
    **Target Variable**: Customer Churn (Binary Classification)
    
    **Features**: 
    - Demographic features (age, gender, city, membership type)
    - Behavioral features (purchases, spending, activity)
    - Engagement features (email opens, app usage, subscription status)
    
    **Preprocessing**:
    - Missing value imputation
    - Categorical encoding
    - Feature scaling
    - SMOTE for class imbalance
    - Feature selection
    """)
    
    st.subheader("Business Impact")
    st.success("""
    This model helps identify customers at risk of churning, enabling:
    
    - **Proactive Retention**: Target high-risk customers before they leave
    - **Cost Optimization**: Focus retention efforts where they're most needed
    - **Revenue Protection**: Reduce customer acquisition costs by retaining existing customers
    - **Personalized Engagement**: Tailor marketing campaigns based on churn risk
    """)


if __name__ == "__main__":
    main()

