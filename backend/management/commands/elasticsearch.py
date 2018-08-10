from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from ...elastic import setup_elasticsearch
from ...models import Item


class Command(BaseCommand):
    help = 'Deal with elasticsearch'
    tasks = ('setup', 'sync')

    def add_arguments(self, parser):
        parser.add_argument('task')

    def handle(self, *args, **options):
        task = options['task']
        if task not in self.tasks:
            raise CommandError('Task "%s" is not a valid task. Valid are: "%s"' % (
                task,
                ', '.join(self.tasks)
            ))

        if task == 'setup':

            def b(val):
                return 'Yes' if val else 'No'

            deleted, created = setup_elasticsearch()

            self.stdout.write('Deleted index "%s": %s' % (settings.ES_INDEX, b(deleted)))
            self.stdout.write('Created index "%s": %s' % (settings.ES_INDEX, b(created)))
            self.stdout.write(self.style.SUCCESS('Setup Elasticsearch: Done.'))

        if task == 'sync':
            for item in Item.objects.all():
                item.sync_elasticsearch()
