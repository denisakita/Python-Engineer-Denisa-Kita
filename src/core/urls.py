from django.urls import path

from core.views import IndexView, FetchDataView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('fetch-data/', FetchDataView.as_view(), name='fetch_data'),

]
