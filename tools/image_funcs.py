from apps.base.models import BaseAbstractModel


def get_image_path(instance: BaseAbstractModel, filename: str):
    """
    Get path for /static/profile_images/{instance_id}/{file_name}
    """
    return f'{instance.__class__.__name__}/{instance.id}/{filename}'
