import numpy as np
import faiss
import glob
from deepface import DeepFace

def extract_features(img_path):
    img_representation = DeepFace.represent(img_path, model_name = 'Facenet')
    img_representation = img_representation[0]['embedding']
    return img_representation

# Create a list of image file paths (you need to provide these)
image_paths = []

image_directory = '/root/Code/Test/retinaface1/storage/*'

for file in glob.glob(image_directory):
    image_paths.append(file)

# Extract features for all images
features = []
for image_path in image_paths:
    feature = extract_features(image_path)
    features.append(feature)

# Convert list of vectors to a 2D array
features = np.array(features).astype('float32')

# Build the index
index = faiss.IndexFlatL2(features.shape[1])
index.add(features)

# Now the index is built, you can use it to perform efficient similarity search and clustering
input_img = extract_features("/root/Code/image/putin.jpg")
input_img = np.array([input_img]).astype('float32')

k = 1
distances, indices = index.search(input_img, k)

if distances[0][0] < 100:
    print(f"Match: {image_paths[indices[0][0]]}, Distance: {distances[0][0]}")