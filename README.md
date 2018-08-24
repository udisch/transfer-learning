An image classifier for several bird species. The species list can be found in `model\output_labels.txt`.

Based on TensorFlow's transfer learning tutorial, with inception v3 as the base model: https://www.tensorflow.org/hub/tutorials/image_retraining

Trained using images obtained from Google image searches, with https://github.com/hardikvasa/google-images-download

Usage:
======

* Requires TensorFlow to be installed

python label_image_server.py


The classifier is wrapped in a REST service. After starting the server, you
can upload images by http:

Using httpie:

`http --form localhost:5000/predict image@/some_bird.jpg`

Using curl:

`curl -X POST -F image=@some_bird.jpg http://localhost:5000/predict`

