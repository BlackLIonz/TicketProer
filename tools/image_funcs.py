import os


def get_profile_image_path(instance: object, filename: str):
    """
    Get path for /static/profile_images/{instance_id}/{file_name}
    """
    return os.path.join('profile_images', instance.id, filename)


def get_place_photo_path(instance: object, filename: str):
    """
    Get path for /static/profile_images/{instance_id}/{file_name}
    """
    return os.path.join('place_photos', instance.id, filename)


def get_posters_path(instance: object, filename: str):
    """
    Gets path for event's poster '/static/posters/{event_id}/{filename}
    """
    return os.path.join('posters', instance.id, filename)
