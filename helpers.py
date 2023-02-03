import uuid as uuid
from werkzeug.utils import secure_filename
import os
UPLOAD_FOLDER = 'static/profile_imgs'


def save_user_images(form):
    """this helper saves images to database then returns the form to create/updata a User"""
    profile_img = form.image_url.data
    background_img = form.header_image_url.data

    # if image_url (users profile pic) not null and file type is allowed
    if profile_img:
        # make sure file name is secure
        profile_img_filename = secure_filename(profile_img.filename)
        # unique naming file with uuid
        db_img_name = str(uuid.uuid1()) + '_' + profile_img_filename
        # change filename on acutual file and save
        profile_img.filename = db_img_name
        profile_img.save(os.path.join(UPLOAD_FOLDER, db_img_name))
        form.image_url.data.filename = profile_img.filename

    # if header_image_url not null and file type is allowed
    if background_img:
        # make sure file name is secure
        background_filename = secure_filename(background_img.filename)
        # unique naming file with uuid
        db_bg_img_name = str(uuid.uuid1()) + '_' + background_filename
        # change filename on acutual file and save
        background_img.filename = db_bg_img_name
        background_img.save(os.path.join(UPLOAD_FOLDER, db_bg_img_name))
        form.header_image_url.data.filename = background_img.filename

    return form


def update_user_images(form, user):
    # check if the user is updating the header image
    background_img = form.header_image_url.data
    if background_img and background_img != user.header_image_url:
        # make sure file name is secure
        background_filename = secure_filename(background_img.filename)
        # unique naming file with uuid
        db_bg_img_name = str(uuid.uuid1()) + '_' + background_filename
        # change filename on acutual file and save
        background_img.filename = db_bg_img_name
        background_img.save(os.path.join(UPLOAD_FOLDER, db_bg_img_name))
        form.header_image_url.filename = background_img.filename
        try:
            os.remove(f'{UPLOAD_FOLDER}/{user.header_image_url}')
        except:
            print('********')
    else:
        form.header_image_url.filename = user.header_image_url
    # check if the user is updating the user image
    profile_img = form.image_url.data
    if profile_img and profile_img != user.image_url:
        # make sure file name is secure
        profile_img_filename = secure_filename(profile_img.filename)
        # unique naming file with uuid
        db_img_name = str(uuid.uuid1()) + '_' + profile_img_filename
        # change filename on acutual file and save
        profile_img.filename = db_img_name
        profile_img.save(os.path.join(UPLOAD_FOLDER, db_img_name))
        form.image_url.filename = profile_img.filename
        try:
            os.remove(f'{UPLOAD_FOLDER}/{user.image_url}')
        except:
            print('***********')
    else:
        form.image_url.filename = user.image_url

    return form
