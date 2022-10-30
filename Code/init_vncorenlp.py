import py_vncorenlp
import os

path = 'vncorenlp'

isExist = os.path.exists(path)
if not isExist:
    os.makedirs(path)

py_vncorenlp.download_model(save_dir='vncorenlp')