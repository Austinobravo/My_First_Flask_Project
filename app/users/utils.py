import os
import secrets
from flask import current_app
from PIL import Image


def save_picture(picture): 
    random= secrets.token_hex(8)
    _,change_name= os.path.splitext(picture.filename)
    new_picture=random+change_name

    saved_pic_path = os.path.join(current_app.root_path,'static\profile_pics', new_picture)
    resize_picture= Image.open(picture)
    resize_picture.thumbnail((125,125))

    resize_picture.save(saved_pic_path)
    return new_picture
