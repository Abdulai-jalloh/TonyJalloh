
import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
print("Starting the flask app..")
app = Flask(__name__)
app.secret_key = 'only those who strong can sovive'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/lands')
def lands():
  json_path = os.path.join(BASE_DIR, 'land.json')
  with open('static/land.json') as f:
    land_data = json.load(f)
    return render_template('AllLands.html', lands = land_data)
  

@app.route('/land/<int:land_id>')
def land_detail(land_id):
    with open('static/land.json') as f:
      land_data = json.load(f)
    
      land = next((i for i in land_data if str(i['id']) == str(land_id)), None)
      if land:
        return render_template('Land-details.html', land=land)
      else:
        return "Land Not Found", 404


@app.route('/contact')
def contact():
      return render_template('Contact.html')

#Folder to store upload images and extension that should be allowed for images
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {
   'png', 'jpg', 'jpeg'
}

def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1) [1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin')
def admin_page():
   if not session.get('admin_logged_in'):
       flash('You most log in first.', 'warning')
       return redirect(url_for('login'))
   return render_template('admin.html')

@app.route('/upload_land',
methods=['GET', 'POST'])
def upload_land():
    if not session.get('admin_logged_in'):
        flash("Vous devez d'abord vous connecter.", 'warning')
        return redirect(url_for('login_page'))
    if request.method == 'POST':
        title = request.form['title']
        location = request.form['location']
        price = request.form['price']
        description = request.form['description']
        Features = request.form.getlist('features')
        mainImage = request.files['mainimage']
        gallery = request.files.getlist('images')
        Name = request.form['name']
        Phone = request.form['phone']
        Email = request.form['email']
        Maps = request.form['map']

        # Save Main Image
        main_image_filename = secure_filename(mainImage.filename)
        main_image_path = os.path.join(app.config['UPLOAD_FOLDER'], main_image_filename).replace('\\', '/')
        mainImage.save(main_image_path)

        # Save Gallery Images
        gallery_files = []
        for index, img in enumerate(gallery):
            if img.filename != '':
                filename = secure_filename(img.filename)
                new_filename = f"{title}-gallery-{index + 1}.jpg"  # Optional: rename neatly
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename).replace('\\', '/')
                img.save(save_path)

                gallery_files.append(save_path)   # Only append once

        # After saving all images, create the new land entry
        new_land = {
            "id": get_next_id(),
            "title": title,
            "location": location,
            "price": price,
            "mainimage": main_image_path,
            "images": gallery_files,
            "features": Features,
            "contact": {
                "name": Name,
                "email": Email,
                "phone": Phone
            },
            "description": description,
            "map": Maps
        }

        # Save to JSON
        try:    
            with open('static/land.json', 'r+') as f:
                try:
                    data = json.load(f)
                except json.decoder.JSONDecodeError:
                    data = []
                data.append(new_land)
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=2)
        except FileNotFoundError:
            with open('static/land.json', 'w') as f:
                json.dump([new_land], f, indent=2)

        flash('Terrain ajouté avec succés!', 'success')
        return redirect(url_for('admin_page'))
    pass
    return render_template('admin.html')

def get_next_id():
             try:
                with open('static/land.json', 'r') as f:
                   data = json.load(f)
                   if data:
                      return data[-1]['id'] + 1
                   else:
                      return 1
             except (FileNotFoundError, json.JSONDecodeError):
              return 1

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        UserName = request.form['username']
        Password = request.form['password']

        if UserName == 'admin' and Password == 'AG23037':
            session['admin_logged_in'] = True
            flash('Connexion réussie!', 'success')
            return redirect(url_for('admin_page'))
        else:
            flash('Connexion invalide, veuillez réessayer.', 'danger')
            return render_template('login.html')
    return render_template('login.html')
if __name__ == '__main__':
      app.run(debug=True)