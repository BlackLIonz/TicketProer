from celery.utils.log import get_task_logger
from celery.task import task

from apps.events.models import Event
from apps.feedbacks.models import Review

logger = get_task_logger(__name__)


@task(name='rating')
def count_rating():
    for event in Event.objects.all():
        event_rating = [review.rating for review in Review.objects.filter(parent_object_id=event.rating).exclude(status=Review.DELETED)]
        if len(event_rating):
            rating = sum(event_rating) / len(event_rating)
            event.rating = rating
            event.save()
        logger.info(f"Counted rating for {event.id} event")
