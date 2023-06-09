import streamlit as st
from PIL import Image
from tensorflow.keras.utils import load_img,img_to_array
import numpy as np
from keras.models import load_model
import requests

model = load_model('FV.h5')
labels = {0: 'apple', 1: 'banana', 2: 'beetroot', 3: 'bell pepper', 4: 'cabbage', 5: 'capsicum', 6: 'carrot',
          7: 'cauliflower', 8: 'chilli pepper', 9: 'corn', 10: 'cucumber', 11: 'eggplant', 12: 'garlic', 13: 'ginger',
          14: 'grapes', 15: 'jalepeno', 16: 'kiwi', 17: 'lemon', 18: 'lettuce',
          19: 'mango', 20: 'onion', 21: 'orange', 22: 'paprika', 23: 'pear', 24: 'peas', 25: 'pineapple',
          26: 'pomegranate', 27: 'potato', 28: 'raddish', 29: 'soy beans', 30: 'spinach', 31: 'sweetcorn',
          32: 'sweetpotato', 33: 'tomato', 34: 'turnip', 35: 'watermelon'}

fruits = ['Apple', 'Banana', 'Bello Pepper', 'Chilli Pepper', 'Grapes', 'Jalepeno', 'Kiwi', 'Lemon', 'Mango', 'Orange',
          'Paprika', 'Pear', 'Pineapple', 'Pomegranate', 'Watermelon']
vegetables = ['Beetroot', 'Cabbage', 'Capsicum', 'Carrot', 'Cauliflower', 'Corn', 'Cucumber', 'Eggplant', 'Ginger',
              'Lettuce', 'Onion', 'Peas', 'Potato', 'Raddish', 'Soy Beans', 'Spinach', 'Sweetcorn', 'Sweetpotato',
              'Tomato', 'Turnip']
calories_dict={'Apple':52}
def calories(prediction):
  cal=calories_dict[prediction]
  return cal

def processed_img(img_path):
  img = load_img(img_path, target_size=(224, 224, 3))
  img = img_to_array(img)
  img = img / 255
  img = np.expand_dims(img, [0])
  answer = model.predict(img)
  y_class = answer.argmax(axis=-1)
  print(y_class)
  y = " ".join(str(x) for x in y_class)
  y = int(y)
  res = labels[y]
  print(res)
  return res.capitalize()
def run():
  st.title("Calorie prediction")
  img_file = st.file_uploader("Choose an Image", type=["jpg", "png"])
  if img_file is not None:
    img = Image.open(img_file).resize((250, 250))
    st.image(img, use_column_width=False)
    save_image_path = '/content/upload' + img_file.name
    with open(save_image_path, "wb") as f:
      f.write(img_file.getbuffer())
    if img_file is not None:
      result = processed_img(save_image_path)
      print(result)
      if result in vegetables:
        st.info('**Category : Vegetables**')
      else:
        st.info('**Category : Fruits**')
      st.success("**Predicted : " + result + '**')
      cal=calories(result)
      #cal = fetch_calories(result)
      if cal:
        st.warning('**' + str(cal) + '(100 grams)**')
run()
