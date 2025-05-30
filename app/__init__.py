from flask import Flask
from app.models import db
from flask_migrate import Migrate  # type: ignore
from flask_wtf.csrf import CSRFProtect
import os
from dotenv import load_dotenv


csrf = CSRFProtect()
migrate = Migrate()

def create_app():
  base_dir = os.path.abspath(os.path.dirname(__file__))
  project_Folder = os.path.abspath(os.path.join(base_dir))
  app = Flask(__name__, 
  template_folder=os.path.join(project_Folder, '..', 'templates'),
  static_folder=os.path.join(project_Folder, '..', 'static'))
  
  load_dotenv(os.path.join(base_dir, '..', '.env'))

  db_path = os.path.join(base_dir, '..', 'instance', 'database.db')
  db_uri = f"sqlite:///{os.path.abspath(db_path)}"

  app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_secret_fallback')

  app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['UPLOAD_FOLDER'] = os.path.join(project_Folder, '..', 'static', 'uploads')
  app.config['IMAGES_FOLDER'] = os.path.join(project_Folder, '..', 'static', 'images')
  app.config['ALLOWED_EXTENSION'] = {'JPG', 'jpeg', 'png'}
  
  instance_dir =  os.path.join(base_dir, '..', 'instance')
  os.makedirs(instance_dir, exist_ok=True)
  if not os.path.exists(db_path):
    open(db_path, 'a').close()

  db.init_app(app)
  csrf.init_app(app)
  migrate.init_app(app, db)


  from app.routes.land_routes import land_bp
  app.register_blueprint(land_bp)
  return app