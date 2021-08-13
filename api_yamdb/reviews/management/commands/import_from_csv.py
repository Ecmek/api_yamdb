import csv
from django.core.management.base import BaseCommand, CommandError
# from polls.models import Question as Poll
# from reviews.models import Title
# import os

# print(os.path.join(os.path.dirname(__file__), '..', 'b', 'titles.csv'))


class Command(BaseCommand):
    help = 'Переносит данные из файла csv в базу данных'

    # def add_arguments(self, parser):  # <-- можно использовать
    #     # Можно использовать для указания количества записей, которые нужно
    #     # перенести.
    #     parser.add_argument('title_ids', nargs='+', type=int)

    #     # Можно прикрутить флаговые аргументы
    #     parser.add_argument(
    #         '-p', '--prefix', type=str, help='Префикс для username'
    #     )
    #     parser.add_argument(
    #         '-a', '--admin',
    #         action='store_true',
    #         help='Создание учетной записи администратора'
    #     )

    def handle(self, *args, **options):
        # Обработка средствами библиотеки csv

        with open('a:/Dev/api_yamdb/api_yamdb/static/data/titles.csv', encoding='utf-8') as file_obj:  # сделать относительный путь к файлу
            reader = csv.DictReader(file_obj, delimiter=',')
            for line in reader:
                print(line["id"])
                print(line["name"])
                print(line["year"])
                print(line["category"])
                # Title.create(name=, year=, category=, genre=None)  # !genre нет в title.csv


# class Command(BaseCommand):
#     help = 'Closes the specified poll for voting'

#     def add_arguments(self, parser):
#         parser.add_argument('poll_ids', nargs='+', type=int)

#     def handle(self, *args, **options):
#         for poll_id in options['poll_ids']:
#             try:
#                 poll = Poll.objects.get(pk=poll_id)
#             except Poll.DoesNotExist:
#                 raise CommandError('Poll "%s" does not exist' % poll_id)

#             poll.opened = False
#             poll.save()

#             self.stdout.write(
#                 self.style.SUCCESS('Successfully closed poll "%s"' % poll_id)
#             )
