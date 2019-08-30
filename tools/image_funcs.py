import os


def get_image_path(instance: object, filename: str):
    """
    Get path for /static/profile_images/{instance_id}/{file_name}
    """
    return f'{instance.__name__}/{instance.id}/{filename}'
