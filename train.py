import sys
import os

script_path = os.path.abspath(__file__)
src_path = os.path.abspath(os.path.join(script_path, '..', '..', 'facenet', 'src'))
aligned_path = os.path.abspath(os.path.join(script_path, '..', 'data', 'aligned'))
#aligned_path = os.path.abspath(os.path.join(script_path, '..', 'data2', 'aligned'))
pb_path = os.path.abspath(os.path.join(script_path, '..', 'models', '20180402-114759/20180402-114759.pb'))
pkl_path = os.path.abspath(os.path.join(script_path, '..', 'models', 'my_classifier.pkl'))
#pkl_path = os.path.abspath(os.path.join(script_path, '..', 'models', 'my_classifier2.pkl'))
cmd = """python {}/classifier.py TRAIN {} {} {} --batch_size 1""".format(src_path, aligned_path, pb_path, pkl_path)
os.system(cmd)
