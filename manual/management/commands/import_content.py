import json
from django.core.management.base import BaseCommand
from django.utils.html import escape
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

                self.create_subsections(section, section_data['subsections'])

            self.stdout.write(
                self.style.SUCCESS('Content imported successfully'))

    def create_subsections(self, parent_section, subsections_data):
        for subsection_data in subsections_data:
            author = User.objects.get(email=subsection_data['author']) if \
                subsection_data['author'] else None

            # Escape HTML content to ensure it is stored correctly
            content = escape(subsection_data['content'])

            subsection, created = Subsection.objects.get_or_create(
                section=parent_section if isinstance(
                    parent_section,Section) else parent_section.section,
                title=subsection_data['title'],
                defaults={
                    'content': content,
                    'author': author,
                    'parent': parent_section if isinstance(
                        parent_section, Subsection) else None
                }
            )

            # Recursively create nested subsections
            self.create_subsections(subsection,
                                    subsection_data['subsections'])
