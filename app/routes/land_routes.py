from flask import Blueprint, app, current_app, render_template, request, redirect, session, url_for, flash
from werkzeug.utils import secure_filename
from app.models import Land, Sale, db
import os
from twilio.rest import Client
from email.message import EmailMessage
import smtplib
from app.forms import LoginForm
from app.forms import ContactForm
from app.forms import AddLandForm
from app.forms import DeleteForm
from app.forms import SellLandForm
from flask import jsonify
land_bp = Blueprint('land', __name__)

# the Contact Messages

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auto_taken = os.getenv('TWILIO_AUTH_TOKEN')
Twilio_number = os.getenv('TWILIO_PHONE_NUMBER')
Admin_number = os.getenv('ADMIN_PHONE_NUMBER')

#whatsapp
twil_whatsapp_num = os.getenv('TWILIO_WHATSAPP_NUMBER')
Admin_whatsapp_num = os.getenv('ADMIN_WHATSAPP_NUMBER')

#Email
email_user = os.getenv('Email_user')
email_password = os.getenv('Email_password')
reciver_email = os.getenv('Reciver_Email')

client = Client(account_sid, auto_taken)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower()in app.config['ALLOWED_EXTENSIONS']

# Stating the routes
@land_bp.route('/')
def home():
  lands = Land.query.filter_by(status='Available', visible=True).all()
  return render_template('index.html', lands=lands)

@land_bp.route('/lands')
def lands():
  lands = Land.query.filter_by(status='Available', visible=True).all()
  return render_template('AllLands.html', lands=lands)

@land_bp.route('/land/<int:land_id>')
def land_details(land_id):
  land = Land.query.get(land_id)
  if land:
    return render_template('Land-details.html', land=land)
  else:
    return "Land Not Found", 404
  
@land_bp.route('/upload_land', 
methods=['GET', 'POST'])
def upload_land():
    form = AddLandForm()
    if request.method == 'POST':
        print("Form sumited")
        print("The form is",form.errors)
        if form.validate_on_submit():
            print("The form is valid")
            try:
               title = form.title.data
               location = form.location.data 
               price = float(form.price.data)
               description = form.description.data
               features = form.features.data
               features_list = [f.strip() for f in features.split(',')]
               main_image = form.mainImage.data
               gallery = form.gallery.data
               status = form.status.data

               # Owner information
               name = form.name.data
               email = form.email.data
               phone = form.phone.data
               latitude = float(form.latitude.data)
               longitude = float(form.longitude.data)
               # Save the main image
               os.makedirs(current_app.config['IMAGES_FOLDER'], exist_ok=True)
               main_filename = secure_filename(main_image.filename).replace(" ", "_")
               main_path = os.path.join(current_app.config['IMAGES_FOLDER'], main_filename).replace("\\", "/")
               try:
                  main_image.save(main_path)
                  main_image_url = f"/static/images/{main_filename}"
                  print("Main image saved successfuly.")
               except Exception as e:
                  print("Error saveing Main images:", e)
                  return "Image save failed: " + str(e), 500

                            # Save gallery images
               gallery_paths = []
               for i, img in enumerate(gallery):
                    if img.filename:
                        filename = secure_filename(img.filename).replace(" ", "_")
                        save_name = f"{title}-gallery-{i+1}-{filename}"
                        path = os.path.join(current_app.config['IMAGES_FOLDER'], save_name).replace("\\", "/")
                        img.save(path)
                        img_url = f"/static/images/{save_name}"
                        gallery_paths.append(img_url)
                        print("Saving image in", path)
                        print("Saving image in", gallery_paths)
                # Now, create the land only once after gathering all images:
               try:
                    new_land = Land(
                        title=title,
                        location=location,
                        price=price,
                        mainImage=main_image_url,
                        gallery=gallery_paths,
                        features=features_list,
                        description=description,
                        status=status,
                        name=name,
                        phone=phone,
                        email=email,
                        latitude=latitude,
                        longitude=longitude
                    )
                    db.session.add(new_land)
                    db.session.commit()
                    flash("Terrain ajouté avec succès!", "success") 
                    print("New land is", new_land)
               except Exception as e:
                    print("Error creating or saving land:", e)
                    
                    print("New land is",new_land)
            except Exception as e:
                return redirect(url_for('land./')) 
        else:
            print("form Validation faild")
            flash("form not submited please check", "denger")
    return render_template('admin.html', form=form) 

@land_bp.route('/dashboard')
def dashboard():
   return render_template('dashboard.html')

@land_bp.route('/Login',
methods=['GET', 'POST'])
def login():
  form = LoginForm()

  if form.validate_on_submit():
    username = form.Name.data
    Password = form.Password.data

    if username == 'admin' and Password == 'AG23037':
      session['admin_logged_in'] = True
      flash('Connection réussie!', 'success')
      return redirect(url_for('land.dashboard'))
    else:
      flash('Connexion invalide, veuillez réessayer.', 'danger')
  return render_template('login.html', form=form)


@land_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        FirstName = form.FirstName.data
        LastName = form.LastName.data
        Phone = form.Phone.data
        Email = form.Email.data
        Message = form.Message.data

        full_infoMessage = (
            f"Message from: {FirstName} {LastName}\n"
            f"Phone: {Phone}\nEmail: {Email}\nMessage: {Message}"
        )

        success = False

        # Try SMS
        try:
            client.messages.create(
                body=full_infoMessage,
                from_=Twilio_number,
                to=Admin_number
            )
            success = True
        except Exception as e:
            print(f"SMS error: {e}")

        # Try WhatsApp
        try:
            client.messages.create(
                body=full_infoMessage,
                from_=twil_whatsapp_num,
                to=Admin_whatsapp_num
            )
            success = True
        except Exception as e:
            print(f"WhatsApp error: {e}")

        # Try Email
        try:
            msg = EmailMessage()
            msg.set_content(full_infoMessage)
            msg['Subject'] = 'Land Contactors'
            msg['From'] = email_user
            msg['To'] = reciver_email

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(email_user, email_password)
                smtp.send_message(msg)
            success = True
        except Exception as e:
            print(f"Email error: {e}")

        if success:
            flash('Thank you for contacting us! We will reach back to you as soon as possible.', 'success')
        else:
            flash('Something went wrong while sending your message. Please try again.', 'danger')

        return redirect(url_for('land.contact'))

    return render_template('Contact.html', form=form)

@land_bp.route('/SellLand',
methods=['GET', 'POST'])
# Improved version
def SellLand():
    form = SellLandForm()
    lands = Land.query.filter_by(status='Available', visible=True).all()
    form.land_id.choices = [(land.id, f"{land.title} - {land.location} - {land.price}") for land in lands]

    if form.validate_on_submit():
        land = Land.query.get(form.land_id.data)
        land.status = 'Sold'

        # Store sale in separate Sale table
        sale = Sale(
            land_id=land.id,
            buyerName=form.buyerName.data,
            phone=form.phone.data,
            sale_date=form.sale_date.data,
        )

        if form.documents.data:
            filename = secure_filename(form.documents.data.filename)
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            form.documents.data.save(upload_path)
            sale.documents = filename

        db.session.add(sale)
        db.session.commit()
        flash('Land Mark as Sold Successfuly', 'success')
        return redirect(url_for('land.dashboard'))
    return render_template('SellLand.html', form=form)
@land_bp.route('/sold_land')
def view_sold_land():
    sold_lands = Sale.query.order_by(Sale.sale_date.desc()).all()
    return render_template('SoldLand.html', sold_lands=sold_lands)

@land_bp.route('/api/lands')
def get_lands():
   lands = Land.query.filter_by(status='Available', visible=True).all()
   print(lands)
   def serialize(land):
      return{
         'id': land.id,
         'title': land.title,
         'location': land.location,
         'price': land.price,
         'description': land.description,
         'mainImage': land.mainImage,
         'gallery': land.gallery,
         'features': land.features,
         'status': land.status,
         'contact': {
            'name': land.name,
            'phone': land.phone,
            'email': land.email
         },
         'date_Added': land.date_Added,
         'latitude': land.latitude,
         'longitude': land.longitude
      }
   return jsonify([serialize(land) for land in lands])
#Route for the page to show all Lands for the admin to work
@land_bp.route('/admin_work')
def Admin_work():
    lands = Land.query.order_by(Land.id.desc()).all() 
    Delete_form = DeleteForm()
    return render_template('Admin_work.html', lands=lands, Delete_form=Delete_form)

#Route for the page to show land details
@land_bp.route('/admin_View/land/<int:land_id>')
def view_land(land_id):
    land = Land.query.get_or_404(land_id)
    return render_template('Land-details.html', land=land)

@land_bp.route('/admin/land/<int:land_id>/edit', 
methods=['GET', 'POST'])
def Edit_land(land_id):
    land = Land.query.get_or_404(land_id)
    form = AddLandForm(obj=land)
    if request.method == 'POST':
        if form.validate_on_submit():
            land.title = form.title.data
            land.location = form.locaton.data
            land.price = float(form.price.data)
            land.description = form.description.data
            land.features = form.features.data
            land.status = form.status.data
            
            #Edit owner Information
            land.name = form.name.data
            land.email = form.email.data
            land.phone = form.phone.data
            land.latitude = float(form.latitude.data)
            land.longitude = float(form.longitude.data)
            #Save MainImages
            if form.mainImage.data:
                main_image = form.mainImage.data
                filename = secure_filename(main_image.filename)
                path = os.path.join(current_app.config['IMAGES_FOLDER'], filename).replace("\\", "/")
                main_image.save(path)
                land.mainImage = filename

            #Save Gallery Images
            if form.gallery.data:
                gallery_url = []
                for i, img in enumerate(form.gallery.data):
                    if img.filename:
                        filename = secure_filename(img.filename)
                        save_gallery = f"{land.title}-gallery-{i+1}-{filename}"
                        gallery_path = os.path.join(current_app.config['IMAGES_FOLDER'], save_gallery).replace("\\", "/")
                        img.save(gallery_path)
                        gallery_url.append(save_gallery)
                        land.gallery = gallery_url

                        db.session.commit()
                        flash("Land Updated Successfully!", "success")
                        return redirect(url_for('admin_work'))
    return render_template('admin.html', form=form, editing=True, land=land)

@land_bp.route('/admin/land/<int:land_id>/delete', 
methods=['POST'])
def delete_land(land_id):
    land = Land.query.get_or_404(land_id)
    land.visible = False
    db.session.commit()
    flash("land deleted successfully.", "success")
    return redirect(url_for('land.Admin_work'))
