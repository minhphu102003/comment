from fuzzywuzzy import process
import re
import json
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import config

def read_data(path):
    with open(path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    comments = []
    labels = []

    # Duyệt qua từng sản phẩm và comment để lấy dữ liệu và dán nhãn 
    for item in data:
        if item['nameProduct']:
            for comment in item.get('comments', []):
                if comment['content'] and 'star' in comment:
                    comments.append(comment['content'])
                    labels.append(1 if comment['star'] > 3 else 0)
    df = pd.DataFrame({
        'comment': comments,
        'label': labels
    })
    return df

def read_aff_file(aff_file):
    replace_map = {}
    with open(aff_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith('MAP'):
                parts = line.split()[1:]
                for part in parts:
                    if '(' in part and ')' in part:
                        key = part[1:-1]
                    else:
                        replace_map[part[:-1]] = part[-1]
    return replace_map


def read_dictionary_file(dic_file):
    dictionary = set()
    with open(dic_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line and not line.isdigit() and not line.isupper():
                dictionary.add(line)
    return dictionary


# ! Hàm này thiếu chuyển từ không dấu sang có dấu, chỉnh sửa ngữ pháp phù hợp với ngữ cảnh 
def find_similar_word(word, dictionary):
    similar_words = {
        "khong": ["không"],
        "tr": ["triệu", "trời"],
        "đt": ["điện thoại"],
        "dt": ["điện thoại"],
        "0k": ["ổn"],
        "ok": ["ổn"],
        "ko":["không"],
        "đc":["được"],
        "dc":["được"],
        "ae": ["anh em"],
        "kg":["không"],
        "đag":["đang"],
        "k":["không"],
        "mn":["mọi người"],
        "nv": ["nhân viên"],
        "ms":["mới"],
        "dk":["được"],
        "đk": ["được"],
        "tgdd": ["thế giới di động"],
        "m": ["mình"],
        "sp": ["sản phẩm"],
        "sd": ["sử dụng"],
        "bt": ["bình thường", "biết"],
        "ns": ["nói"],
        "bh": ["bây giờ"],
        "củ": ["triệu"],
        "e" : ["em"],
        "good": ["tốt"],
        "ktra": ["kiểm tra"],
        "mnh": ["mình"],
        "z": ["vậy"],
        "cam": ["camera"],
        "j": ["gì"],
        "ad": ["admin"],
        "nvien":["nhân viên"],
        "trc": ["trước"],
        "ng": ["người"],
        "ngta": ["người ta"],
        "shop":["sốp"],
        "fai":["phải"],
        "okla":["rất ổn"],
        "tot": ["tốt"],
        "s": ["sao"],
        "oke": ["ổn"],
        "game":["game"],
        "km": ["khuyến mãi"],
        "zoom": ["thu phóng"],
        "box": ["hộp"],
        "mlem":["ngon"],
        "kh": ["không"],
        "nt": ["nhắn tin"],
        "chup":["chụp"],
        "vs": ["so với"],
        "tgdđ": ["thế giới di động"],
        "online":["trực tuyến"],
        "bin": ["pin"],
        "xai":["sai"],
        "n/v":["nhân viên"],
        "e": ["em"],
        "s/p": ["sản phẩm"],
        "ak": ["à"],
        "cg": ["cũng"],
        "r": ["rồi"],
        "nge":["nghe"],
        "ktv":["cộng tác viên"],
        "pẩm":["phẩm"],
        "wa": ["quá"],
        "h":["giờ"],
        "mess": ["messager"],
        "mk":["mình"],
        "ddc":["được"],
        "fb":["facebook"],
        "ji":["gì"],
        "oce": ["ổn"],
        "very": ["rất"],
        "nhìu": ["nhiều"],
    }
    if word in similar_words:
        return similar_words[word][0]  
    else:
        return word


def spell_check_vietnamese(comment, replace_map, dictionary):
    corrected_comment = []
    words = re.findall(r'\w+|[^\w\s]', comment, re.UNICODE)
    
    for word in words:
        if word.isalpha() and word.lower() not in dictionary:
            original_word = word
            word = word.lower()
            
            if word in replace_map:
                word = replace_map[word]
                
            if word in dictionary:
                corrected_comment.append(original_word)
            else:
                similar_word = find_similar_word(word, dictionary)
                corrected_comment.append(similar_word)
        else:
            corrected_comment.append(word)
    
    return ' '.join(corrected_comment)

def main():

    df = read_data(config.json_path)

    replace_map = read_aff_file(config.aff_file)
    dictionary = read_dictionary_file(config.dic_file)

    df['corrected_comment'] = df['comment'].apply(lambda x: spell_check_vietnamese(x, replace_map, dictionary))

    df.to_excel(config.correct_comment_path, index=False)     

if __name__ == '__main__':
    main()
