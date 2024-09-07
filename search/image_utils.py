import numpy as np
import os
from PIL import Image
from search.logger import logger
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet import preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Load ResNet50 pre-trained model without the top classification layer
resnet_model = ResNet50(weights='imagenet', include_top=False, pooling='avg', input_shape=(224, 224, 3))
    

def extract_embedding(image_path):
    print('getCWT')
    print(os.getcwd())
    image = load_img(image_path, target_size=(224, 224))
    image_array = img_to_array(image)
    image_array = np.expand_dims(image_array, axis=0)
    image_array = preprocess_input(image_array)
    
    # Extract embeddings
    embedding = resnet_model.predict(image_array)
    print('returned from extract_embedding')
    return embedding.squeeze()  # Flatten the output to 1D


