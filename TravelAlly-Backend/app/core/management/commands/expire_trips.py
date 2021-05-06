from django.core.management.base import BaseCommand
from core.models import Trip
from datetime import datetime, timedelta


class Command(BaseCommand):

    help = 'Expires trip objects which are out-of-date'

    def handle(self, *args, **options):
        print("here")
        Trip.objects.filter(start_time__lte=datetime.now()-timedelta(days=1)).delete()
