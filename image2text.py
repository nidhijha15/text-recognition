import io
import os
#import scipy.misc
import numpy as np
import six
#import time
import glob
#from IPython.display import display
import cv2

from six import BytesIO

#import matplotlib
#import matplotlib.pyplot as plt
from PIL import Image
import pytesseract as pt
from pdf2image import convert_from_path

import tensorflow as tf
from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

#get_ipython().run_line_magic('matplotlib', 'inline')


# %%
MODEL_NAME = 'inference_graph'
#IMAGE_NAME = 'aPICT0001.JPG'
#pics = list()
#ch = 0;


# %%
PATH_TO_LABELS = 'static/model/label_map.pbtxt'
NUM_CLASSES = 1


# %%
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


# %%
tf.keras.backend.clear_session()
model = tf.saved_model.load(f'static/model/saved_model')


# %%
def load_image_into_numpy_array(path):
  """Load an image from file into a numpy array.

  Puts image into numpy array to feed into tensorflow graph.
  Note that by convention we put it into a numpy array with shape
  (height, width, channels), where channels=3 for RGB.

  Args:
    path: a file path (this can be local or on colossus)

  Returns:
    uint8 numpy array with shape (img_height, img_width, 3)
  """
  img_data = tf.io.gfile.GFile(path, 'rb').read()
  image = Image.open(BytesIO(img_data))
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

# %%
def run_inference_for_single_image(model, image):
    image = np.asarray(image)
  # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
    input_tensor = tf.convert_to_tensor(image)
  # The model expects a batch of images, so add an axis with `tf.newaxis`.
    input_tensor = input_tensor[tf.newaxis,...]

  # Run inference
    model_fn = model.signatures['serving_default']
    output_dict = model_fn(input_tensor)

  # All outputs are batches tensors.
  # Convert to numpy arrays, and take index [0] to remove the batch dimension.
  # We're only interested in the first num_detections.
    num_detections = int(output_dict.pop('num_detections'))
    output_dict = {key:value[0, :num_detections].numpy() 
                 for key,value in output_dict.items()}
    output_dict['num_detections'] = num_detections

  # detection_classes should be ints.
    output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)
   
  # Handle models with masks:
    if 'detection_masks' in output_dict:
    # Reframe the the bbox mask to the image size.
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
            output_dict['detection_masks'], output_dict['detection_boxes'],
            image.shape[0], image.shape[1])      
        detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5,
                                       tf.uint8)
        output_dict['detection_masks_reframed'] = detection_masks_reframed.numpy()
    
    return output_dict


# %%
def display_text(path):
  image_path = path
  image_np = cv2.imread(image_path)
  #image_np = load_image_into_numpy_array(image_path)
  output_dict = run_inference_for_single_image(model, image_np)
  boxes = output_dict['detection_boxes']
  scores = output_dict['detection_scores']
  classes = output_dict['detection_classes']
  min_score_thresh = 0.2
  bboxes = boxes[scores > min_score_thresh]
  im_width = image_np.shape[1]
  im_height = image_np.shape[0]
  final_box = []
  count = 0
  for box in bboxes:
      ymin, xmin, ymax, xmax = box
      final_box.append([xmin * im_width, xmax * im_width, ymin * im_height, ymax * im_height])
      count += 1
  #print(final_box)
  text = []
  configuration = ("-l eng --oem 1 --psm 6")
  for i in range(len(final_box)):
      x1 = int(final_box[i][0])
      y1 = int(final_box[i][2])
      x2 = int(final_box[i][1])
      y2 = int(final_box[i][3])
      crop_img = image_np[y1:y2, x1:x2]
      #image_p = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
      #image_p = cv2.medianBlur(image_p, 5)
      #image_p = cv2.adaptiveThreshold(image_p, 245, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 115, 1)
      text.append(pt.image_to_string(crop_img, config = configuration).replace('\n',' ').replace('\x0c',' '))
  return text
def display_image(path):
  image_np = load_image_into_numpy_array(path)
  im_width = image_np.shape[0]
  output_dict = run_inference_for_single_image(model, image_np)
  vis_util.visualize_boxes_and_labels_on_image_array(
      image_np,
      output_dict['detection_boxes'],
      output_dict['detection_classes'],
      output_dict['detection_scores'],
      category_index,
      instance_masks=output_dict.get('detection_masks_reframed', None),
      use_normalized_coordinates=True,
      min_score_thresh=0.3,
      line_thickness=2,
      skip_scores=False,
      skip_labels=True,)
  img = Image.fromarray(image_np)
  return img
def doc_text(path):   
    pages = convert_from_path(path, fmt = 'jpeg')
    output = ""
    text = ""
    for page in pages:
        text = pt.image_to_string(page)
        output += text
    return output

# %%
