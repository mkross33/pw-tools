from messaging.utils import get_noobs, filter_noobs
from django.core.management.base import BaseCommand
from messaging.models import Message


# gets the 200 newest members of PW not in VM, not inactiev, and not in an alliance. Then sends them a recruitment
# message. CRON to run every hour to stay competative with the bots of other alliances, however it can be run
# manually if necessary via 'python manage.py recruit'
class Command(BaseCommand):
    help = 'Updates the member table and makes new member logs'

    def handle(self, *args, **kwargs):
        small_nations = get_noobs()
        contacts = filter_noobs(small_nations)
        message = Message.objects.get(category='recruitment')
        for contact in contacts:
            message.send(contact)
