An image classifier for several bird species. The species list can be found in `model\output_labels.txt`.

Based on TensorFlow's transfer learning tutorial, with inception v3 as the base model: https://www.tensorflow.org/hub/tutorials/image_retraining

Trained using images obtained from Google image searches, with https://github.com/hardikvasa/google-images-download

git-lfs is used for storing the model, it must be installed https://git-lfs.github.com

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


Deployment
==========

https://tecadmin.net/install-angular-on-ubuntu/

1) Make sure model folder contains the full model and not git lfs shortcut
1) create virtualenv
2) pip install -r requirements.txt
3) to run backend: gunicorn -w1 label_image_server:app
4) frontend on static folder: npm install, use angular cli for build
5) nginx

* if gunicorn is endlessly starting workers - not enough memory


