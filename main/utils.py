import csv
from django.http import HttpResponse
import codecs

class ExportModel(object):
    @staticmethod
    def as_csv(meta):
        """
        :param meta: (dict) keys should be
        'file' (string: absolute path),
        'queryset' a Django QuerySet instance,
        'fields' a list or tuple of field model field names (strings)
        meta = {
            'file': '/devices.csv',
            'class': Device,
            'fields': ('name',)
        }
        :returns (string) path to file
        """
        with open(meta['file'], 'w+') as f: 
            writer = csv.writer(f)
            writer.writerow(meta['fields'])
            for obj in meta['queryset']:
                row = [str(getattr(obj, field))
                       for field in meta['fields']]
                writer.writerow(row)
            path = f.name
        return path


def get_model_as_csv_file_response(meta, content_type):
    with open(ExportModel.as_csv(meta), 'r') as f:
        response = HttpResponse(f.read(), content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename=%s' % f.name.split('/')[-1:][0]
        # response.write(u'\ufeff'.encode('utf8'))
        response.write(codecs.BOM_UTF8)
    return response
