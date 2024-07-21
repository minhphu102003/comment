import re

# Danh sách tên sản phẩm (cần chỉnh sửa theo danh sách thực tế của bạn)
product_names = ["23ul", "ui6", "1", "sóp"]

def remove_product_names(text, product_names):
    # Xóa các tên sản phẩm trong danh sách
    for product in product_names:
        text = re.sub(r'\b' + re.escape(product) + r'\b', '', text, flags=re.IGNORECASE)
    return text

def remove_numeric_characters(text):
    # Xóa các ký tự chứa số
    return re.sub(r'\d', '', text)

def remove_punctuation(text):
    # Xóa các dấu phẩy và các dấu câu không cần thiết
    return re.sub(r'[^\w\s]', '', text)

def remove_icons(text):
    # Xóa các icon (emoji)
    emoji_pattern = re.compile(
        "["u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def preprocess_text(text, product_names):
    text = remove_product_names(text, product_names)
    text = remove_numeric_characters(text)
    text = remove_punctuation(text)
    text = remove_icons(text)
    text = text.lower()  # Chuyển tất cả thành chữ thường
    text = ' '.join(text.split())  # Loại bỏ khoảng trắng thừa
    return text

if __name__ == "__main__":
    pass

