import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, train_test_split, cross_val_score
from imblearn.over_sampling import RandomOverSampler
import pickle

# Load your data
data = pd.read_csv('./cleaned_file.csv')

# 1. Handle Missing Data
# Impute missing numerical data with mean
numerical_cols = ['Deaths', 'Death Rate', 'Age Adjusted Death Rate']
num_imputer = SimpleImputer(strategy='mean')
data[numerical_cols] = num_imputer.fit_transform(data[numerical_cols])

# Impute missing categorical data with the most frequent value
categorical_cols = ['Leading Cause', 'Sex', 'Race Ethnicity']
cat_imputer = SimpleImputer(strategy='most_frequent')
data[categorical_cols] = cat_imputer.fit_transform(data[categorical_cols])

# 2. Assign the target column first
y = data['Leading Cause']  # 'Leading Cause' is the target column

# 3. Now drop the 'Leading Cause' column for the features
X = data.drop(columns=['Leading Cause'])

# 4. Handle categorical columns: one-hot encode 'Race Ethnicity'
X = pd.get_dummies(X, columns=['Race Ethnicity'], drop_first=True)

# 5. Handle binary categorical column 'Sex' using Label Encoding
label_encoder = LabelEncoder()
X['Sex'] = label_encoder.fit_transform(X['Sex'])

# 6. Save the LabelEncoder and Race Ethnicity columns for future use
with open('label_encoder_sex.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)

# Save the column names for Race Ethnicity after one-hot encoding (to ensure consistency during prediction)
race_columns = X.columns.tolist()
with open('race_columns.pkl', 'wb') as f:
    pickle.dump(race_columns, f)

# 7. Handle Data Imbalance with Random Over-Sampling
ros = RandomOverSampler(sampling_strategy='auto', random_state=42)
X_res, y_res = ros.fit_resample(X, y)

# 8. Scale numerical features (important: scale only after resampling)
scaler = StandardScaler()
X_res[['Death Rate', 'Age Adjusted Death Rate']] = scaler.fit_transform(X_res[['Death Rate', 'Age Adjusted Death Rate']])

# Save the scaler for numerical columns (to be used during prediction)
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

# 9. Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.2, random_state=42)

# 10. Train a Random Forest Classifier
model = RandomForestClassifier(random_state=42)

# Hyperparameter tuning using RandomizedSearchCV
param_dist = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
}
random_search = RandomizedSearchCV(model, param_distributions=param_dist, n_iter=10, cv=5, random_state=42)
random_search.fit(X_train, y_train)

# Print best hyperparameters found
print(f'Best parameters: {random_search.best_params_}')

# Cross-validation accuracy
cv_scores = cross_val_score(random_search.best_estimator_, X_train, y_train, cv=5, scoring='accuracy')
print(f'Cross-validation accuracy: {cv_scores.mean()}')

# 11. Save the trained model to a file
with open('random_search_model.pkl', 'wb') as f:
    pickle.dump(random_search.best_estimator_, f)
