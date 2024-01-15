from django.urls import path

from people.utils import aggregate_data_view, template_view
from people.views import inspect_dataset

urlpatterns = [
    path('inspect-dataset/<int:dataset_id>/', inspect_dataset, name='inspect'),
    path('aggregate_data_view/', aggregate_data_view, name='aggregate_data_view'),
    path('template/', template_view, name='template_view'),

]
