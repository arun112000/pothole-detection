import numpy as np
import os
import tensorflow as tf
from PIL import Image
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

MODEL_NAME = 'trained-inference-graphs/ssd_inception5000'
CWD_PATH = os.getcwd()
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')
PATH_TO_LABELS = os.path.join(CWD_PATH,'annotations','label_map.pbtxt')
NUM_CLASSES = 1
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)
 
 
config = tf.ConfigProto()
config.gpu_options.allow_growth=True

# Load tensorflow model
detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')
  sess = tf.Session(graph=detection_graph,config=config)

# Function to detect and draw bounding boxes
def model_predict(image_path):
    image = Image.open(image_path)
    image_np = np.array(image)
    image_np_expanded = np.expand_dims(image_np, axis=0)
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    scores = detection_graph.get_tensor_by_name('detection_scores:0')
    classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
    (boxes, scores, classes, num_detections) = sess.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=1,
        min_score_thresh=0.30)
    # Save image with bounding boxes
    Image.fromarray(image_np).save(image_path[:-4]+'_detected'+'.jpeg')
    # Return 1 if pothole is found
    if scores[0][0]>0.3:
        return 1
    else:
        return 0

# Function to make prediction on image using API
@app.route('/', methods=['POST'])
def predict_api():
    data = request.get_json(force=True)
    f = Image.open(requests.get(data['file_path'], stream = True).raw)
    f.save('temp.jpg')
    prediction = model_predict('temp.jpg')
    return jsonify(prediction)

if __name__ == "__main__":
    app.run(debug=True,use_reloader=False)
