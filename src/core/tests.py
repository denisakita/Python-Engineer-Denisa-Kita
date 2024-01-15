from datetime import datetime

from django.test import TestCase

from core.models import SWAPICollectionDataset


class SWAPICollectionDatasetModelTest(TestCase):
    def setUp(self):
        # Create a sample SWAPICollectionDataset instance for testing
        self.dataset = SWAPICollectionDataset.objects.create(
            filename='test_dataset.csv',
            download_date=datetime.now(),
        )

    def test_model_fields(self):
        self.assertEqual(self.dataset._meta.get_field('filename').max_length, 255)
        self.assertEqual(self.dataset._meta.get_field('download_date').auto_now_add, False)

    def test_model_str_method(self):
        self.assertEqual(str(self.dataset), 'test_dataset.csv')

    def test_model_verbose_names(self):
        self.assertEqual(SWAPICollectionDataset._meta.verbose_name, 'SWAPICollection')
        self.assertEqual(SWAPICollectionDataset._meta.verbose_name_plural, 'SWAPICollections')

    def test_model_db_table(self):
        self.assertEqual(SWAPICollectionDataset._meta.db_table, 'swapi_collections')
