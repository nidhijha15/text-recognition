## Text Recognition and Document Scanner
The text recognition application is for everyone who wants to scan texts from images or
documents. It has a simple and user-friendly interface, allowing the user to easily interact
with the software. It can read various image formats (.jpeg, .jpg, .png...) and supports both
monochromatic and colored images.

## How does it work?
This application is made using Tensorflow, Python, and Flask. It consists of a tensorflow pre-trained model which has been trained to detect texts in images. 
The text detected is then cropped and send to Pytesseract to read. The read reconginsed can then be searched on Google or Amazon. 

The Document Scanner works on a similar manner, the pages of the pdf uploaded are converted into images and send to the PyTesseract to read, the text recognised in the 
images are then showed in a editable-format.

## Features

### Text Detection
These are a few of the results of the text detection using the TensorFlow Model:

![alt text](https://github.com/nidhijha15/text-recognition/blob/master/static/upload/pic1.jpg)
![alt text](https://github.com/nidhijha15/text-recognition/blob/master/static/upload/pic2.jpg)

### Text Recognition and GUI

This is the homepage of Flask-based homepage
![alt text](https://github.com/nidhijha15/text-recognition/blob/master/static/upload/Screenshot%20from%202020-11-20%2010-46-31.png)

This is how the text recognition works:

![alt text](https://github.com/nidhijha15/text-recognition/blob/master/static/upload/text_recog.png)

After the text is recognised in the image it can be searched on Google.

![alt text](https://github.com/nidhijha15/text-recognition/blob/master/static/upload/g_text.png)

This is how the Document Scanner works

![alt text](https://github.com/nidhijha15/text-recognition/blob/master/static/upload/d_recog.png)

## How to Use?

1. Clone the respositary
2. Open the terminal in the project directory
3. Run this command: python application.py
4. Open the http://localhost:5000/ in a browser
5. Enjoy converting images into text!







