import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

from preprocessing import load_and_prepare_data

# Load data
df = load_and_prepare_data("data/Bengaluru_House_Data.csv")

X = df[
    [
        'location',
        'log_total_sqft',
        'location_density',
        'infrastructure_score'
    ]
]

y = df['price_per_sqft']

# Feature groups
cat_features = ['location']
num_features = [
    'log_total_sqft',
    'location_density',
    'infrastructure_score'
]

# Preprocessing
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), num_features),
    ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features)
])

# Model
model = RandomForestRegressor(
    n_estimators=400,
    max_depth=25,
    min_samples_split=5,
    min_samples_leaf=3,
    random_state=42,
    n_jobs=-1
)

pipeline = Pipeline([
    ('preprocessing', preprocessor),
    ('model', model)
])

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train
pipeline.fit(X_train, y_train)

# Evaluate
preds = pipeline.predict(X_test)
print("R2 Score:", r2_score(y_test, preds))
print("MAE:", mean_absolute_error(y_test, preds))

# Save model
joblib.dump(pipeline, "model/land_model.pkl")
