from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Lae MNIST andmed
X, y = fetch_openml('mnist_784', version=1, return_X_y=True, as_frame=False)
X = X / 255.0  # Skaleeri piksliväärtused vahemikku 0-1

# Jaga andmed treening- ja testkomplektideks
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Loo mudel
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Treeni mudel
model.fit(X_train, y_train)

# Hinda mudeli täpsust testandmetel
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f'Mudeli täpsus: {accuracy:.2f}')

# Salvesta mudel diskile
joblib.dump(model, 'digit_model.pkl')
