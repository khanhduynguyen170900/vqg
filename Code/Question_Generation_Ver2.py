import py_vncorenlp
from utils import *
import json
vncorenlp_path = __file__.replace('Question_Generation_Ver2.py', 'vncorenlp')
pattern_path = __file__.replace('Question_Generation_Ver2.py', '../pattern/pattern.txt')
# input_path = '../../io/input.txt'

# model = py_vncorenlp.VnCoreNLP(save_dir=vncorenlp_path)

with open(pattern_path, "r") as f:
    patterns = f.read().split('\n')

text = "Tiếp đến là dạng địa hình núi thấp , đồi thấp xen kẽ bình nguyên và thung lũng , thỉnh thoảng có núi đá chạy ra sát biển , chia cắt dải đồng bằng ven biển thành những vùng đồng bằng nhỏ hẹp , với chiều dài 200km bờ biển khúc khuỷu có điều kiện thuận lợi để hình thành các cảng nước sâu , nhiều vùng đất rộng thuận lợi để lập khu chế xuất và khu công nghiệp tập trung ."

# with open(input_path, "r") as f:
#     text = f.read()

# annotated_text = model.annotate_text(text)

from vncorenlp import VnCoreNLP
annotator = VnCoreNLP(address="http://127.0.0.1", port=9000)


# To perform word segmentation, POS tagging, NER and then dependency parsing
annotated_text = annotator.annotate(text)
annotated_text = annotated_text['sentences']
tmp = {}
for i, at in enumerate(annotated_text):
    tmp[i] = at
annotated_text = tmp

print(question_generation(annotated_text, patterns))
