from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename
import os
import image2text as it

application = app = Flask(__name__)

app.config['SECRET_KEY'] = 'fb7103394e2c8f1f152cc0a2ed83ccdb'
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',title = "Home")

app.config["IMAGE_UPLOADS"] = "static/upload"
app.config["DOC_UPLOADS"] = "static/upload"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG"]
app.config["MAX_IMAGE_FILESIZE"] = 10* 1024 * 1024
app.config["MAX_DOC_FILESIZE"] =  50* 1024 * 1024
app.config["ALLOWED_DOC_EXTENSIONS"] = ["PDF"]

def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

def generating_url(text):

    output = text.replace(" ","+")
    url1 = "http://www.google.com/search?q="+output
    url2 = "https://www.amazon.in/s?k="+output+"&ref=nb_sb_noss_2"
    return [url1, url2]


def allowed_doc(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_DOC_EXTENSIONS"]:
        return True
    else:
        return False

def clean_up(text):
    print(text)
    res = ""
    print(text)
    for i in text:
        print(i)
        if i.strip().isalnum == False :
            continue
        else:
            res += i
    if res.strip() == "":
        return "No Text Detected"
    else:
        return res.strip(" ")

def allowed_image_filesize(filesize, filename):
    print(int(filesize))
    print(filename)
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

def allowed_doc_filesize(filesize):
    if int(filesize) <= app.config["MAX_DOC_FILESIZE"]:
        return True
    else:
        return False

@app.route("/image", methods = ["GET","POST"])
def image():
    output = ''
    if request.method == "POST":
        if request.files:
            if "filesize" in request.cookies:
                image = request.files["image"]
                if image.filename == "":
                    return render_template('image.html',title = "Image to Text", output = "Error: No file")
                if not allowed_image_filesize(request.cookies["filesize"], image.filename):
                    return render_template('image.html',title = "Image to Text", output = "Error: Exceeds Size")
                if allowed_image(image.filename) == False:
                    return render_template('image.html',title = "Image to Text", output = "Error: Not Allowed Extension")
                else: 
                    print("Image Saved")
                    filename = image.filename
                    print(filename)
                    image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    path = app.config["IMAGE_UPLOADS"] + "/"+filename
                    new_path = app.config["IMAGE_UPLOADS"] + "/"+filename[:-4]+"_text.jpg"
                    print("Image Saved")
                    it.display_image(path).save(new_path)
                    text = it.display_text(path)
                    output += clean_up(text)
                    url1 = generating_url(output)[0]
                    url2 = generating_url(output)[1]
                    #os.remove(path)
                    return render_template('image.html',title = "Image to Text",output = output, filename = image.filename[:-4]+"_text.jpg", url1 = url1, url2 = url2)
    return render_template('image.html',title = "Image to Text") 
@app.route("/doc", methods = ["GET","POST"])
def doc():
    if request.method == "POST":
        print("hello")
        if request.files:
            if "filesize" in request.cookies:
                if not allowed_doc_filesize(request.cookies["filesize"]):
                    return render_template('doc.html',title = "Document to Text" , output = "Error: Exceeds Size")
                doc = request.files["doc"]
                if doc.filename == "":
                    return render_template('doc.html',title = "Document to Text", output = "Error: No file")
                if allowed_doc(doc.filename) == False:
                    return render_template('doc.html',title = "Document to Text", output = "Error: Not Allowed Extension")
                else: 
                    print("Doc Saved")
                    filename = secure_filename(doc.filename)
                    doc.save(os.path.join(app.config["DOC_UPLOADS"], filename))
                    path = app.config["DOC_UPLOADS"] + "/"+filename
                    text = it.doc_text(path)
                    os.remove(path)
                    return render_template('doc.html',title = "Document to Text" ,text = text)    
    return render_template('doc.html',title = "Document to Text")

if __name__ == '__main__':
    app.run(debug=True)