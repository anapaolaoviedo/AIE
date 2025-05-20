# example_model.py

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 🚩 Missing: class_weight='balanced' → class imbalance
# 🚩 No SHAP or LIME → lack of explainability
# ✅ Includes validation

# Dummy data
X = [[0, 1], [1, 0], [1, 1], [0, 0]]
y = [0, 1, 1, 0]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

model = LogisticRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, predictions))