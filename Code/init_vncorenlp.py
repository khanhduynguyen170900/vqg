import py_vncorenlp
import os

path = __file__.replace('init_vncorenlp.py', 'vncorenlp')

isExist = os.path.exists(path)
if not isExist:
    os.makedirs(path)

py_vncorenlp.download_model(save_dir=path)
