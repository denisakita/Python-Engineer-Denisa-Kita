import csv
import os

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from config import settings
from core.models import SWAPICollectionDataset


def inspect_dataset(request, dataset_id):
    # Retrieve the dataset based on the provided dataset_id or return a 404 response if not found.
    dataset = get_object_or_404(SWAPICollectionDataset, id=dataset_id)
    filename = dataset.filename
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    # Read the CSV file and convert it to a list of dictionaries for further processing.
    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        cleaned_data = [{k: v for k, v in row.items()} for row in csv_reader]

    """ we can change per_page 10 but load more button will be disabled because all csv has 10 rows  """
    # Set the number of rows to display per page.
    per_page = 5
    paginator = Paginator(cleaned_data, per_page)
    page = request.GET.get('page', 1)

    try:
        formatted_data = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, default to the first page.
        formatted_data = paginator.page(1)
    except EmptyPage:
        # If the page parameter is out of range, deliver the last page of results.
        formatted_data = paginator.page(paginator.num_pages)

    # Check if there are more pages available for pagination.
    has_next = formatted_data.has_next()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # If it's an AJAX request, return JSON response for dynamic update
        return JsonResponse({
            'html': render_to_string('load_more_row.html', {'formatted_data': formatted_data}),
            'has_next': has_next,
        })

    # Prepare context for rendering the HTML page.
    context = {
        'csv_filename': dataset.filename,
        'csv_download_date': dataset.download_date,
        'formatted_data': formatted_data,
        'has_next': has_next,
        'page': int(page),
        'dataset': dataset,
    }

    # Render the HTML page and return the response.
    return render(request, 'people.html', context)
