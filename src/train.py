import pandas as pd
from preprocessing import preprocess_text

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import config

# Đọc dữ liệu đã sửa lỗi chính tả từ file Excel
df = pd.read_excel(config.correct_comment_path)

# Danh sách tên sản phẩm (cần chỉnh sửa theo danh sách thực tế của bạn)
product_names = ["23ul", "ui6", "sóp"]

# Tiền xử lý các bình luận
df['preprocessed_comment'] = df['corrected_comment'].apply(lambda x: preprocess_text(x, product_names))

# Lưu kết quả vào file Excel
df.to_excel(config.preprocessed_comments_path, index=False)
 