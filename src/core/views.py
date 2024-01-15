import csv
import os
from datetime import datetime
from typing import List, Dict

import petl as etl
import requests
from django.core.management import BaseCommand
from django.http import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from config import settings
from core.const import CHARACTERS_URL
from core.models import SWAPICollectionDataset
from people.models import SWAPIPeopleModel


class IndexView(TemplateView):
    template_name = 'index.html'

    """ Override the get_context_data method to include additional context data."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collections'] = SWAPICollectionDataset.objects.all()
        return context


class SWAPIDataFetcher:
    """ Fetch data from a given URL and return it as a JSON object."""

    @staticmethod
    def fetch_data(url):
        response = requests.get(url)
        return response.json()


class SWAPIDataProcessor:
    """ Process characters data received from SWAPI, including date formatting and field manipulation."""

    @staticmethod
    def process_data(characters_data):
        characters_table = etl.fromdicts(characters_data['results'])
        characters_table = etl.addfield(characters_table, 'date',
                                        lambda row: datetime.strptime(row['edited'], '%Y-%m-%dT%H:%M:%S.%fZ')
                                        .strftime('%Y-%m-%d'))
        characters_table = etl.convert(characters_table, 'homeworld', BaseSWAPICollectionDownloader.resolve_planet_name)
        characters_table = etl.cutout(characters_table, 'films', 'species', 'vehicles', 'starships', 'created',
                                      'edited')

        return list(etl.dicts(characters_table))


class BaseSWAPICollectionDownloader(BaseCommand):
    help = 'Base class for downloading Star Wars dataset'

    """ Resolve the name of the planet from the given planet URL."""

    @staticmethod
    def resolve_planet_name(planet_url):
        planet_response = SWAPIDataFetcher.fetch_data(planet_url)
        return planet_response.get('name', 'Unknown')

    """ Fetch characters data from the specified URL, process it, save it to CSV and database."""

    def fetch_and_store_data(self, characters_url):
        try:
            characters_data = SWAPIDataFetcher.fetch_data(characters_url)
            cleaned_data = SWAPIDataProcessor.process_data(characters_data)

            filename = self.save_to_csv(cleaned_data)
            self.save_to_database(cleaned_data, filename)

            return filename
        except Exception as e:
            print(f"Error during data fetch and storage: {e}")
            raise

    """ Save cleaned data to a CSV file and return the filename."""

    @staticmethod
    def save_to_csv(cleaned_data):
        filename = f'star_wars_dataset_{timezone.now().strftime("%Y%m%d%H%M%S")}.csv'
        file_path = os.path.join(settings.MEDIA_ROOT, filename)

        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=cleaned_data[0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(cleaned_data)

        return filename

    """ Save cleaned data to the database and create a corresponding dataset entry."""

    @staticmethod
    def save_to_database(cleaned_data, filename):
        SWAPIPeopleModel.objects.bulk_create(
            [SWAPIPeopleModel(**data) for data in cleaned_data],
            ignore_conflicts=True
        )

        dataset = SWAPICollectionDataset(filename=filename, download_date=timezone.now())
        dataset.save()


class FetchDataView(View):
    """ Override the dispatch method to exempt CSRF for this view."""

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    """ Handle GET request to retrieve datasets and return a JSON response."""

    def get(self, request, *args, **kwargs):
        try:
            datasets = SWAPICollectionDataset.objects.all()
            data_list = self.create_data_list(datasets)
            return JsonResponse({'datasets': data_list}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    """ Handle POST request to fetch and store new data, then return the updated datasets in a JSON response."""

    def post(self, request, *args, **kwargs):
        try:
            download_command = BaseSWAPICollectionDownloader()
            filename = download_command.fetch_and_store_data(CHARACTERS_URL)

            datasets = SWAPICollectionDataset.objects.all()
            data_list = self.create_data_list(datasets)

            return JsonResponse({'datasets': data_list}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    """ Create a list of dictionaries containing dataset information."""

    @staticmethod
    def create_data_list(datasets: List[SWAPICollectionDataset]) -> List[Dict]:
        return [
            {'id': dataset.id,
             'name': dataset.filename,
             'date': dataset.download_date} for dataset in datasets
        ]
