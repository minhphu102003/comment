import joblib
import pandas as pd

# Tải mô hình và vectorizer đã lưu
model = joblib.load('sentiment_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Ví dụ về cách sử dụng mô hình để dự đoán trên dữ liệu mới
new_comments = [
    "Máy rất tốt, pin trâu",
    "Dịch vụ tệ, không đáng tiền"
]

# Tiền xử lý và vector hóa văn bản mới
X_new = vectorizer.transform(new_comments)

# Dự đoán
predictions = model.predict(X_new)

# In kết quả dự đoán
for comment, prediction in zip(new_comments, predictions):
    sentiment = 'Tích cực' if prediction == 1 else 'Tiêu cực'
    print(f'Comment: {comment} => Sentiment: {sentiment}')