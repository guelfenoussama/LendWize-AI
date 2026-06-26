import pickle
from flask import Flask, request, jsonify
from waitress import serve

# 1. Load the Models and Vectorizers
classifier_file = 'best_classifier_model.bin'
regressor_file = 'best_regressor_model.bin'

with open(classifier_file, 'rb') as f_in_c:
    dv, best_classifier_model = pickle.load(f_in_c)

with open(regressor_file, 'rb') as f_in_r:
    dvd, best_regressor_model = pickle.load(f_in_r)



# 2. Start Flask Server and API Routes
app = Flask('loan_service')

@app.route('/predict', methods=['POST'])
def predict():
    customer = request.get_json()
   
    X_class = dv.transform([customer])
    y_pred_proba = best_classifier_model.predict_proba(X_class)[0][1]
    loan_approved = y_pred_proba >= 0.5
    
    result = {
        'approval_probability': f"{y_pred_proba * 100:.2f}%",
        'loan_approved': bool(loan_approved),
        'expected_amount': 0.0,
        'dscr_status': 'N/A',
        'expected_amount_range': "$0 - $0"
    }
    
    if loan_approved:
        X_reg = dvd.transform([customer])
        expected_amount = best_regressor_model.predict(X_reg)[0]
        
        loan_amount = customer.get('_loan_amount', 0)
        income = customer.get('_income_annum', 1)
        
        if expected_amount > loan_amount:
            expected_amount = loan_amount
        # Calculate the expected loan range (+/- 5%)
        upper_bound = round(expected_amount * 1.05, -3)
        lower_bound = round(expected_amount * 0.95, -3)

        if upper_bound > loan_amount:
            upper_bound = loan_amount
        result['expected_amount'] = float(round(expected_amount, -3))
        # DSCR Check:
        # If the user's income is more than the expected loan amount,
        # the status is 'Healthy'. If not, it is a 'Risk'.
        result['dscr_status'] = 'Healthy' if income > expected_amount else 'Risk'
        
        result['expected_amount_range'] = f"${lower_bound:,.0f} - ${upper_bound:,.0f}"
    else:
        result['dscr_status'] = 'Rejected from Classifier'
        
    return jsonify(result)

#3. Run the Server using Waitress
if __name__ == "__main__":
    print("Server is running on port 9697...")
    serve(app, host='0.0.0.0', port=9697)