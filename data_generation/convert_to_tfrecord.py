# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# source: https://github.com/sararob/tswift-detection/blob/master/convert_to_tfrecord.py

import os
import io
import xml.etree.ElementTree as ET
import tensorflow as tf

from PIL import Image


flags = tf.app.flags
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
flags.DEFINE_string('images_dir', '', 'Path to directory of images')
flags.DEFINE_string('labels_dir', '', 'Path to directory of labels')
FLAGS = flags.FLAGS

# helper functions
# https://github.com/tensorflow/models/blob/master/research/object_detection/utils/dataset_util.py
def int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def int64_list_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))

def bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def bytes_list_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=value))

def float_list_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))


def create_tf_example(example):
    image_path = os.path.join(FLAGS.images_dir, example)
    labels_path = os.path.join(FLAGS.labels_dir, os.path.splitext(example)[0] + '.xml')

    # Read the image
    img = Image.open(image_path)
    width, height = img.size
    img_bytes = io.BytesIO()
    img.save(img_bytes, format=img.format)

    height = height
    width = width
    encoded_image_data = img_bytes.getvalue()
    image_format = img.format.encode('utf-8')

    # Read the label XML
    tree = ET.parse(labels_path)
    root = tree.getroot()
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for object_ in root.iter('object'):
        bbox = object_.find('bndbox')
        class_ = object_.find('class')

        xmins.append(float(bbox.find('xmin').text))
        xmaxs.append(float(bbox.find('xmax').text))
        ymins.append(float(bbox.find('ymin').text))
        ymaxs.append(float(bbox.find('ymax').text))

        classes_text.append(class_.find('text').text.encode('utf-8'))
        classes.append(int(class_.find('label').text))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': int64_feature(height),
        'image/width': int64_feature(width),
        'image/filename': bytes_feature(example.encode('utf-8')),
        'image/source_id': bytes_feature('overlay.py'.encode('utf-8')),
        'image/encoded': bytes_feature(encoded_image_data),
        'image/format': bytes_feature(image_format),
        'image/object/bbox/xmin': float_list_feature(xmins),
        'image/object/bbox/xmax': float_list_feature(xmaxs),
        'image/object/bbox/ymin': float_list_feature(ymins),
        'image/object/bbox/ymax': float_list_feature(ymaxs),
        'image/object/class/text': bytes_list_feature(classes_text),
        'image/object/class/label': int64_list_feature(classes),
    }))
    return tf_example


def main(_):
    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)

    for filename in os.listdir(FLAGS.images_dir):
        tf_example = create_tf_example(filename)
        writer.write(tf_example.SerializeToString())

    writer.close()


if __name__ == '__main__':
    tf.app.run()