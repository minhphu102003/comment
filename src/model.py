import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import config

# Đọc dữ liệu đã tiền xử lý từ file Excel
df = pd.read_excel(config.preprocessed_comments_path)

# Loại bỏ các dòng trống sau khi tiền xử lý
df = df[df['preprocessed_comment'].str.strip().astype(bool)]

# Loại bỏ các hàng có giá trị NaN
df = df.dropna(subset=['preprocessed_comment'])

# Vector hóa văn bản
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['preprocessed_comment'])
y = df['label']

# Chia dữ liệu thành tập huấn luyện và kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Huấn luyện mô hình Logistic Regression
model = LogisticRegression(max_iter=config.epochs)
model.fit(X_train, y_train)

# Dự đoán trên tập kiểm tra
y_pred = model.predict(X_test)

# Đánh giá mô hình
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f'Accuracy: {accuracy:.2f}')
print('Classification Report:')
print(report)

# Lưu mô hình và vectorizer
joblib.dump(model, 'sentiment_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')