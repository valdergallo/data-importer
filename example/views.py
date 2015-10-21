from data_importer.views import DataImporterForm
from data_importer.importers import CSVImporter
from example.models import Person


class ExampleCSVImporter(CSVImporter):
    class Meta:
        model = Person
        delimiter = ';'
        ignore_first_line = True


class DataImporterCreateView(DataImporterForm):
        extra_context = {'title': 'Create Form Data Importer',
                         'template_file': 'myfile.csv',
                         'success_message': "File uploaded successfully"}
        importer = ExampleCSVImporter
