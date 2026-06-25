#Here we will iport the libraeies and the modules we need
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
import pandas as pd
import pickle
from xgboost import XGBClassifier
from xgboost import XGBRegressor

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer

from sklearn.metrics import roc_auc_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import log_loss

from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression


from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor


from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("data/ousssama_dataset_backup_copy.zip")

# Data Cleaning
df = df.drop(columns=['loan_id'])
df.columns = df.columns.str.lower().str.replace(' ', '_')

df['_self_employed'] = df['_self_employed'].str.strip().str.lower().str.replace(' ', '_')
df['_education'] = df['_education'].str.strip().str.lower().str.replace(' ', '_')
df['_loan_status'] = df['_loan_status'].str.strip().str.lower().str.replace(' ', '_')


df._self_employed = (df._self_employed == 'yes').astype(int)
df._education = (df._education == 'graduate').astype(int)
df._loan_status = (df._loan_status == 'approved').astype(int)
#Dataset Splitting
df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=1)
df_train, df_val = train_test_split(df_full_train, test_size=0.25, random_state=1)

df_train = df_train.reset_index(drop=True)
df_val = df_val.reset_index(drop=True)
df_test = df_test.reset_index(drop=True)

y_train = df_train._loan_status.values
y_val = df_val._loan_status.values
y_test = df_test._loan_status.values

del df_train['_loan_status']
del df_val['_loan_status']
del df_test['_loan_status']

dicts = df_train.to_dict(orient='records')
dictss = df_val.to_dict(orient='records')

dv = DictVectorizer(sparse=False)
X_train = dv.fit_transform(dicts)
X_val = dv.transform(dictss)



# Training Classification Models


# 1. Baseline Logistic Regression
model_logistic = LogisticRegression(C=100, max_iter=1000)
model_logistic.fit(X_train, y_train)


#2. Decision Tree Classifier
model_dt = DecisionTreeClassifier(max_depth=5, min_samples_leaf=100)
model_dt.fit(X_train, y_train)


# 3. Random Forest Classifier
model_rfc = RandomForestClassifier(n_estimators=175, max_depth=10, min_samples_leaf=1, random_state=1)
model_rfc.fit(X_train, y_train)


# 4. XGBoost Classifier
xgb_model = XGBClassifier(
    n_estimators=100,
    eta=0.2,
    max_depth=5,
    min_child_weight=1,
    objective='binary:logistic', 
    eval_metric='auc',
    random_state=1
)
xgb_model.fit(X_train, y_train)



#Data Preparation for Regression Models
df_reg = df[df['_loan_status'] == 1]

df_reg_full_train, df_reg_test = train_test_split(df_reg, test_size=0.2, random_state=1)
df_reg_train, df_reg_val = train_test_split(df_reg_full_train, test_size=0.25, random_state=1)

df_reg_train = df_reg_train.reset_index(drop=True)
df_reg_val = df_reg_val.reset_index(drop=True)
df_reg_test = df_reg_test.reset_index(drop=True)

t_train = df_reg_train._loan_amount.values
t_val = df_reg_val._loan_amount.values
t_test = df_reg_test._loan_amount.values

columns_to_drop = ['_loan_status', '_loan_amount']
df_reg_train = df_reg_train.drop(columns=columns_to_drop, errors='ignore')
df_reg_val = df_reg_val.drop(columns=columns_to_drop, errors='ignore')
df_reg_test = df_reg_test.drop(columns=columns_to_drop, errors='ignore')

dits = df_reg_train.to_dict(orient='records')
ditss = df_reg_val.to_dict(orient='records')

dvd = DictVectorizer(sparse=False)
X2_train = dvd.fit_transform(dits)
X2_val = dvd.transform(ditss)


# 1. Baseline Linear Regression
model_lin = LinearRegression()
model_lin.fit(X2_train, t_train)


# 2. Decision Tree Regressor
model_dtr = DecisionTreeRegressor(max_depth=4, min_samples_leaf=15, random_state=1)
model_dtr.fit(X2_train, t_train)


# 3. Random Forest Regressor
rfr_model = RandomForestRegressor(n_estimators=40, max_depth=5, min_samples_leaf=10, random_state=1)
rfr_model.fit(X2_train, t_train)


# 4. XGBoost Regressor
final_xgb_model = XGBRegressor(
    n_estimators=175,
    learning_rate=0.1,
    min_child_weight=50,
    max_depth=2,
    random_state=1
)
final_xgb_model.fit(X2_train, t_train)


# Selecting and saving the Best Models
classification_models = [model_logistic, model_dt, model_rfc, xgb_model]

best_loss = float('inf')

best_classifier_model = None


for model in classification_models:
    y_pred_proba = model.predict_proba(X_val)
    current_loss = log_loss(y_val, y_pred_proba)

    
    if current_loss < best_loss:
        best_loss = current_loss
        best_classifier_model = model


classifier_output_file = 'best_classifier_model.bin'
with open(classifier_output_file, 'wb') as f_out:
    pickle.dump((dv, best_classifier_model), f_out)

regression_models = [model_lin, model_dtr, rfr_model, final_xgb_model]


best_rmse = float('inf')
best_regressor_model = None


for model in regression_models:
    t_pred = model.predict(X2_val)
    rmse_score = np.sqrt(mean_squared_error(t_val, t_pred))
    
    
    if rmse_score < best_rmse:
        best_rmse = rmse_score
        best_regressor_model = model

regressor_output_file = 'best_regressor_model.bin'
with open(regressor_output_file, 'wb') as f_out:
    pickle.dump((dvd, best_regressor_model), f_out)

