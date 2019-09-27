from celery.utils.log import get_task_logger
from celery.task import task
from apps.subscriptions.models import Subscription

logger = get_task_logger(__name__)


@task(name='delete_subscriptions')
def delete_subscriptions(event_id):
    Subscription.objects.filter(event=event_id).exclude(status=Subscription.STATUS_ACTIVE).delete()
    logger.info(f'Not approved subscriptions deleted')
