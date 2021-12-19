import numpy as np
import json
import tensorflow as tf
from annoy import AnnoyIndex
from PIL import Image
import requests
from io import BytesIO
import os

IMAGE_WIDTH = 224
IMAGE_HEIGHT = 224
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

model = None
feature_extractor = None
ann_index = []
ann_metadata = []
MODEL = os.path.join(os.path.dirname(__file__),'xception_224x224.h5')

labels = ['Cell_Phones_and_Accessories', 'Clothing_Men', 'Clothing_Women', 'Electronics', 'Home_and_Kitchen', 'Pet_Supplies', 'Shoes', 'Watches']

def load_model():
    global model, feature_extractor

    model = tf.keras.models.load_model(MODEL)
    # print(model.summary())

    layer_name = 'global_average_pooling2d_2'
    feature_extractor = tf.keras.models.Model(inputs=model.input, outputs=model.get_layer(layer_name).output)

def load_ann_index():
    global ann_index, ann_metadata

    for i in range(len(labels)):
        ann_index_name = 'index_xception_224x224_adam_batch32_8labels_5000each_10ep_ft16ep_label_{}.ann'.format(i)
        ann_metadata_name = 'metadata_xception_224x224_adam_batch32_8labels_5000each_10ep_ft16ep_label_{}.json'.format(i)
        path_ann_index = os.path.join(os.path.dirname(__file__),'./data_model/annoy_index/label_separated/' + ann_index_name)
        path_ann_metadata = os.path.join(os.path.dirname(__file__),'./data_model/annoy_index/label_separated/' + ann_metadata_name)

        with open(path_ann_metadata) as f:
            ann_metadata_data = json.load(f)
            ann_metadata.append(ann_metadata_data)
        
        ann_index_obj = AnnoyIndex(ann_metadata_data['features_length'], metric='angular')
        ann_index_obj.load(path_ann_index)
        ann_index.append(ann_index_obj)

def get_neighbors(label, input, max_neighbors=10):
    results = []

    ann_index_obj = ann_index[label]

    for item_id in ann_index_obj.get_nns_by_vector(input, max_neighbors, search_k=10):
        results.append({
            'id': item_id,
            'asin': ann_metadata[label]['list_asin'][item_id],
        })
    return results

def load_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img_array = np.array(img)
    return img_array

def preprocess_input(x):
    x = tf.image.resize(x, (IMAGE_WIDTH, IMAGE_HEIGHT))
    x = (255 - x) / 255.0
    x = tf.reshape(x, (1, IMAGE_WIDTH, IMAGE_HEIGHT, 3))
    return x

def recommend(url):
    global model, feature_extractor, ann_index, ann_metadata

    top_k = ''

    if feature_extractor is None or model is None:
        load_model()

    if len(ann_index) == 0 or len(ann_metadata) == 0:
        load_ann_index()

    image_raw = load_image(url)
    image = preprocess_input(image_raw)

    prediction_probs = model.predict(image)
    prediction_label = np.argmax(prediction_probs, axis=1)[0]

    input_feature_vector = feature_extractor.predict(image)
    input_feature_vector = input_feature_vector.flatten()
    input_feature_vector = input_feature_vector / input_feature_vector.max()

    top_k = get_neighbors(prediction_label, input_feature_vector)

    return top_k