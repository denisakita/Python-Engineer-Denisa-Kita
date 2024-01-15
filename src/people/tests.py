# tests.py

from datetime import datetime

from django.test import TestCase

from people.models import SWAPIPeopleModel


class SWAPIPeopleModelTest(TestCase):
    def setUp(self):
        self.person = SWAPIPeopleModel.objects.create(
            name='Luke Skywalker',
            height='172',
            mass='77',
            hair_color='blond',
            skin_color='fair',
            eye_color='blue',
            birth_year='19BBY',
            gender='male',
            homeworld='https://swapi.dev/api/planets/1/',
            url='https://swapi.dev/api/people/1/',
            date=datetime.now()
        )

    def test_model_str_method(self):
        self.assertEqual(str(self.person), 'Luke Skywalker')
