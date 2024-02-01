from django.core.management.base import BaseCommand
from geo_outlet.utils import scrape_and_save_to_db

class Command(BaseCommand):
    help = 'Scrape Subway locations and save to the database'

    def handle(self, *args, **options):
        website_url = 'https://subway.com.my/find-a-subway'
        num_locations = 400
        scrape_and_save_to_db(website_url, num_locations)
        self.stdout.write(self.style.SUCCESS('Successfully scraped and saved data.'))