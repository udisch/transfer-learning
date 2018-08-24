# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
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
# ==============================================================================

# based on https://github.com/tensorflow/tensorflow/raw/master/tensorflow/examples/label_image/label_image.py

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse

import numpy as np
import tensorflow as tf
import flask

# initialize Flask
app = flask.Flask(__name__)

# globals
graph = None
model_file = "model/output_graph.pb"
label_file = "model/output_labels.txt"
input_height = 299
input_width = 299
input_mean = 0
input_std = 255
input_layer = "Placeholder"
output_layer = "final_result"

def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph


def read_tensor_from_image_file(file_name,
                                file,
                                input_height=299,
                                input_width=299,
                                input_mean=0,
                                input_std=255):
  output_name = "normalized"
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(
        file, channels=3, name="png_reader")
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(
        tf.image.decode_gif(file, name="gif_reader"))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file, name="bmp_reader")
  else:
    image_reader = tf.image.decode_jpeg(
        file, channels=3, name="jpeg_reader")
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0)
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)

  return result


def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label

def label_image(file_name, file):
  t = read_tensor_from_image_file(
      file_name,
      file,
      input_height=input_height,
      input_width=input_width,
      input_mean=input_mean,
      input_std=input_std)

  input_name = "import/" + input_layer
  output_name = "import/" + output_layer
  input_operation = graph.get_operation_by_name(input_name)
  output_operation = graph.get_operation_by_name(output_name)

  with tf.Session(graph=graph) as sess:
    results = sess.run(output_operation.outputs[0], {
        input_operation.outputs[0]: t
    })
  results = np.squeeze(results)

  top_k = results.argsort()[-5:][::-1]
  labels = load_labels(label_file)
  predictions = []
  for i in top_k:
    predictions.append({"label": labels[i], "probability": float(results[i])})
  return predictions

@app.route("/predict", methods=["POST"])
def predict():
  if flask.request.method == "POST":
        if flask.request.files.get("image"):
            image_obj = flask.request.files["image"]
            file_name = image_obj.filename
            file = image_obj.read()
            predictions = label_image(file_name, file)
            return flask.jsonify(predictions)
        else:
          return "Missing Image"
  else:
    return "Bad request"
  

if __name__ == "__main__":
  graph = load_graph(model_file)
  print("Loaded model")
  app.run()
  