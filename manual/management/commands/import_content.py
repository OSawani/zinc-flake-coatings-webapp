import json
from django.core.management.base import BaseCommand
from manual.models import Section, Subsection
from core.models import User


class Command(BaseCommand):
    help = 'Import content into the manual app'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str,
                            help='The JSON file to import')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']

        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                section_data = item['section']
                author = User.objects.get(email=section_data['author']) if \
                    section_data['author'] else None

                section, created = Section.objects.get_or_create(
                    title=section_data['title'],
                    defaults={
                        'description': section_data['description'],
                        'author': author,
                    }
                )

                for subsection_data in section_data['subsections']:
                    subsection_author = User.objects.get(
                        email=subsection_data['author']) if subsection_data[
                        'author'] else None

                    Subsection.objects.get_or_create(
                        section=section,
                        title=subsection_data['title'],
                        defaults={
                            'content': subsection_data['content'],
                            'author': subsection_author,
                            'parent': None
                            # Adjust if your JSON includes parent subsections
                        }
                    )

        self.stdout.write(self.style.SUCCESS('Content imported successfully'))
