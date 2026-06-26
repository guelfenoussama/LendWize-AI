import streamlit as st
import requests
import os

#1. Initialize Streamlit page settings and set up the logo image path
st.set_page_config(
    page_title="LendWise AI • Oussama Group", 
    page_icon="🏦", 
    layout="centered"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(BASE_DIR, "assets", "logo.png")


#2. Custom CSS to design the app layout and colors
st.markdown("""
    <style>
        /* Style and position for the top logo and brand name header */
        .top-header {
            display: flex;
            align-items: center;
            position: absolute;
            top: -50px;
            left: -20px;
        }
        
        .header-brand {
            color: #007A64;
            font-size: 24px;
            font-weight: 700;
            font-family: 'Inter', sans-serif;
            margin-left: 10px;
        }
        
        /* Style for the big main title (headline) on the page */
        .hero-tagline {
            color: #007A64; 
            font-size: 3.2rem;
            font-weight: 800;
            text-align: center;
            line-height: 1.1;
            margin-top: 60px;
            margin-bottom: 10px;
        }
        /* Style for the smaller text below the main title */
        .hero-sub {
            color: #007A64; 
            text-align: center;
            font-size: 1.4rem;
            font-weight: 500;
            margin-bottom: 40px;
        }
        /* Style for gray background boxes that group input fields */
        .section-box {
            background-color: var(--background-secondary-color);
            color: var(--text-color);
            padding: 20px;
            border-radius: 16px;
            border-left: 5px solid #007A64;
            margin-bottom: 25px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
        }
        /* Style for the main button (Green color and round corners) */
        div.stButton > button:first-child {
            background-color: #007A64 !important;
            color: white !important;
            border-radius: 30px !important;
            border: none !important;
            font-weight: 700 !important;
            padding: 14px 30px !important;
            font-size: 18px !important;
            transition: 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,122,100,0.15);
        }
        div.stButton > button:first-child:hover {
            background-color: #005c4b !important;
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(0,122,100,0.25);
        }
        /* Style for my footer message at the bottom of the page */
        .custom-footer {
            background-color: var(--background-secondary-color);
            color: var(--text-color);
            padding: 20px;
             border-radius: 15px;
            text-align: center;
            border: 1px solid var(--border-color);
            margin-top: 60px;
}
        }
    </style>
""", unsafe_allow_html=True)


#3. Display the app logo and name if found, otherwise show a default bank icon
if os.path.exists(logo_path):
    col_logo, col_space = st.columns([1, 4])
    with col_logo:
        st.image(logo_path, width=45)
    st.markdown("""
        <div class="top-header" style="left: 45px; top: -47px;">
            <span class="header-brand">LendWise AI</span>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="top-header">
            <span style="font-size:30px; margin-right:10px;">🏦</span>
            <span class="header-brand">LendWise AI</span>
        </div>
    """, unsafe_allow_html=True)

#4. Display the main title and th text below using the pre-defined CSS styles
st.markdown("<div class='hero-tagline'>Check Your Loan Approval Chances in Seconds.</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-sub'>Smart Loan Intelligence • Optimized for the Indian Banking Ecosystem using Real-World Financial Data</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


st.markdown("<div class='section-box'><h3>👤 Applicant Information & Profile</h3></div>", unsafe_allow_html=True)


#5. Create data input fields with specific ranges set from the dataset, styled with our custom containers
col1, col2, col3 = st.columns(3)
with col1:
    no_of_dependents = st.number_input("Dependents", min_value=0, max_value=10, value=2)
with col2:
    education = st.selectbox("Education Level", options=["Graduate", "Not Graduate"])
with col3:
    self_employed = st.selectbox("Self Employed?", options=["No", "Yes"])

col_cibil, col_term = st.columns(2)
with col_cibil:
    cibil_score = st.number_input("CIBIL Credit Score", min_value=300, max_value=900, value=700)
with col_term:
    loan_term = st.number_input("Term (Months)", min_value=1, max_value=20, value=12)

col_inc, col_amt = st.columns(2)
with col_inc:
    income_annum = st.number_input("Annual Income (₹)", min_value=200000, max_value=10000000, value=500000, step=1000)
with col_amt:
    loan_amount = st.number_input("Loan Amount Requested (₹)", min_value=300000, max_value=40000000, value=500000, step=1000)

st.markdown("<br><div class='section-box'><h3>🏦 Asset Valuation Portfolio</h3></div>", unsafe_allow_html=True)
col_a1, col_a2 = st.columns(2)
with col_a1:
    residential_assets_value = st.number_input("Residential Assets (₹)", min_value=-100000, max_value=30000000, value=10000, step=1000)
    luxury_assets_value = st.number_input("Luxury Assets (₹)", min_value=300000, max_value=40000000, value=1500000, step=1000)
with col_a2:
    commercial_assets_value = st.number_input("Commercial Assets (₹)", min_value=0, max_value=20000000, value=5000, step=1000)
    bank_asset_value = st.number_input("Bank Value Asset (₹)", min_value=0, max_value=15000000, value=8000, step=1000)

st.markdown("<br>", unsafe_allow_html=True)


#6. Create a clean dictionary mapping all inputs to the correct field names.
if st.button("Browse Loan Insights ➔", use_container_width=True):
    customer_data = {
        "no_of_dependents": int(no_of_dependents),
        "_income_annum": int(income_annum),
        "_loan_amount": int(loan_amount),
        "_loan_term": int(loan_term),
        "_cibil_score": int(cibil_score),
        "_residential_assets_value": int(residential_assets_value),
        "_commercial_assets_value": int(commercial_assets_value),
        "_luxury_assets_value": int(luxury_assets_value),
        "_bank_asset_value": int(bank_asset_value),
        "_education": str(education),       
        "_self_employed": str(self_employed)          
    }



#7. Send the dictionary as JSON to the Flask API for model prediction    
    try:
        response = requests.post("http://localhost:9697/predict", json=customer_data)


#8. Check if the API request succeeded (Status 200), then convert the JSON response into a Python dictionary        
        if response.status_code == 200:
            res_data = response.json()
            st.markdown("### 🔍 Evaluation Dashboard")
            
            dscr_status = res_data.get('dscr_status', 'N/A')


#9. Evaluate the model's decision and display the final approval or decline results to the user            
            if res_data['loan_approved']:
                st.success(f"✅ **LendWise Approved** (Confidence: {res_data['approval_probability']})")
                
                m1, m2 = st.columns(2)
                with m1:
                    st.metric(label="Expected Amount", value=f"₹{res_data['expected_amount']:,.2f}")
                with m2:
                    if "Healthy" in dscr_status or "Low" in dscr_status:
                        st.markdown(f"🟢 **Risk Assessment:** <span style='color:#007A64; font-weight:bold; font-size:1.2rem;'>{dscr_status}</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"🟡 **Risk Assessment:** <span style='color:#D97706; font-weight:bold; font-size:1.2rem;'>{dscr_status}</span>", unsafe_allow_html=True)
                        
                st.info(f"💡 **Dynamic Range:** {res_data['expected_amount_range']}")
            else:
                st.error(f"❌ **LendWise Declined** (Confidence: {res_data['approval_probability']})")
                st.markdown(f"🔴 **Risk Assessment / Reason:** <span style='color:#DC2626; font-weight:bold; font-size:1.2rem;'> High Risk Profile Detected by predictive model.</span>", unsafe_allow_html=True)
        else:
            st.error(f"Server Alert: Status {response.status_code}")

            
#10. If the Flask server is turned off, show an error instead of crashing       
    except requests.exceptions.ConnectionError:
        st.error("Error: Could not establish a secure link with the AI model.")

st.markdown("""
    <div class='custom-footer'>
        <p style='color: #4A5568; margin: 0; font-size: 15px; font-weight: 600;'>
            BROUGHT TO YOU BY OUSSAMA GROUP
        </p>
    </div>
""", unsafe_allow_html=True)