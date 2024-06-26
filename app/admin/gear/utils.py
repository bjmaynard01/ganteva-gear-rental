from app.gear.models import GearCategories, GearItem
import uuid
import os
from flask import current_app, flash
from PIL import Image
from app import db

def get_category_names():
    #categories = GearCategories.query.with_entities(GearCategories.name).all()
    categories = GearCategories.query.all()
    return categories  

def save_img(uploaded_image):
    rand_uuid = str(uuid.uuid4())
    stripped_uuid = rand_uuid.replace('-', '')
    _, f_ext = os.path.splitext(uploaded_image.filename)
    image_name = stripped_uuid + f_ext
    save_path = os.path.join(current_app.root_path, 'static/img/gear', image_name)
    uploaded_image.save(save_path)
    thumb = Image.open(uploaded_image)
    thumb.thumbnail((100, 100))
    fname, _ = os.path.splitext(image_name)
    thumb_name = fname + '_thumb' + f_ext
    thumb_path = os.path.join(current_app.root_path, 'static/img/gear', thumb_name)
    thumb.save(thumb_path)
    

    return image_name, thumb_name

def clear_gear_table():
    items = GearItem.query.all()
    for item in items:
        db.session.delete(item)
    db.session.commit()

    pic_dir = os.path.join(current_app.root_path, 'static/img/gear')
    pics = os.listdir(pic_dir)
    for pic in pics:
        if pic.endswith(".jpg") or pic.endswith(".png"):
            os.remove(os.path.join(pic_dir, pic))

def delete_gear_img(image, thumb):
    img_path = os.path.join(current_app.root_path, 'static/img/gear')
    if image.endswith(".jpg") or image.endswith(".png"):
        os.remove(os.path.join(img_path, image))
    if thumb.endswith(".jpg") or thumb.endswith(".png"):
        os.remove(os.path.join(img_path, thumb))

def get_item_img_path(item):
    return os.path.join(current_app.root_path, 'static/img/gear', item)






