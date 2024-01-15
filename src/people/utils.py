import petl as etl
from django.shortcuts import render

from people.models import SWAPIPeopleModel


def aggregate_data(selected_columns):
    data = SWAPIPeopleModel.objects.values(*selected_columns)
    data_list = list(data)
    table = etl.fromdicts(data_list)

    # Aggregate the data based on selected columns
    key_columns = tuple(selected_columns)
    aggregated_table = etl.aggregate(table, key=key_columns, aggregation=len)

    # Convert the aggregated table to a list of dictionaries
    aggregated_data = list(aggregated_table)

    return aggregated_data


def aggregate_data_view(request):
    selected_columns_str = request.GET.get('selected_columns', '')
    selected_columns_list = selected_columns_str.split(',')
    aggregated_data = aggregate_data(selected_columns_list)

    return render(request, 'counts_fields.html', {
        'aggregated_data': aggregated_data,
    })


def template_view(request):
    model_fields = [field.name for field in SWAPIPeopleModel._meta.get_fields() if field.name != 'id']
    return render(request, 'aggregate_data.html', {'model_fields': model_fields})
