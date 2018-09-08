#!/bin/bash
cd `dirname $0`
path=`pwd`
path=${path%/*}
tf_path=${path%/*}
x="/facenet/src"
src_path=$path$x
echo $src_path
export PYTHONPATH=$PYTHONPATH:$src_path
echo $PYTHONPATH
python $src_path/align/align_dataset_mtcnn.py /home/tao/tensorflow/face_ws/data/raw /home/tao/tensorflow/face_ws/data/aligned --image_size 182 --margin 44 --gpu_memory_fraction 0.25
