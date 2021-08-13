import csv
from django.shortcuts import get_object_or_404
from django.core.management.base import BaseCommand  # , CommandError
# from polls.models import Question as Poll
from reviews.models import Category, Comment, Genre, Review, Title, User
# import os

# print(os.path.join(os.path.dirname(__file__), '..', 'b', 'titles.csv'))


class Command(BaseCommand):
    help = 'Переносит данные из файла csv в базу данных'  # Александр Иванов: "желательно, чтобы ревьюер смог воспроизвести БД :slightly_smiling_face:"

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

        # ______________CATEGORY______________
        try:
            with open('a:/Dev/api_yamdb/api_yamdb/static/data/category.csv', encoding='utf-8') as file_obj:  # сделать относительный путь к файлу
                reader = csv.DictReader(file_obj, delimiter=',')
                for line in reader:
                    # print(line["id"])
                    # print(line["name"])
                    # print(line["slug"])

                    if Category.objects.filter(pk=line['id']).exists():
                        obj = Category.objects.get(pk=line['id'])
                        obj.name = line['name']
                        obj.slug = line['slug']
                        obj.save()
                    else:
                        Category.objects.create(
                            name=line['name'],
                            slug=line['slug']
                        )
        finally:
            file_obj.close()

        # ______________TITLE______________
        try:
            with open('a:/Dev/api_yamdb/api_yamdb/static/data/titles.csv', encoding='utf-8') as file_obj:  # сделать относительный путь к файлу
                reader = csv.DictReader(file_obj, delimiter=',')
                for line in reader:
                    # print(line['id'])
                    # print(line['name'])
                    # print(line['year'])
                    # print(line['category'])

                    category = get_object_or_404(Category, pk=line['category'])

                    if Title.objects.filter(pk=line['id']).exists():
                        obj = Title.objects.get(pk=line['id'])
                        obj.name = line['name']
                        obj.year = line['year']
                        obj.category = category
                        # title.genre = ???  # !genre нет в title.csv
                        obj.save()
                    else:
                        Title.objects.create(
                            name=line['name'],
                            year=line['year'],
                            category=category
                            # genre=???
                        )  # !genre нет в title.csv
        finally:
            file_obj.close()

        # ______________USER______________
        try:
            with open('a:/Dev/api_yamdb/api_yamdb/static/data/users.csv', encoding='utf-8') as file_obj:  # сделать относительный путь к файлу
                reader = csv.DictReader(file_obj, delimiter=',')
                for line in reader:
                    # print(line['id'])
                    # print(line['username'])
                    # print(line['email'])
                    # print(line['role'])
                    # print(line['bio'])
                    # print(line['first_name'])
                    # print(line['last_name'])

                    if User.objects.filter(pk=line['id']).exists():
                        obj = User.objects.get(pk=line['id'])
                        obj.username = line['username']
                        obj.email = line['email']
                        obj.role = line['role']
                        obj.bio = line['bio']
                        obj.first_name = line['first_name']
                        obj.last_name = line['last_name']
                        obj.save()
                    else:
                        User.objects.create(
                            pk=line['id'],
                            username=line['username'],
                            email=line['email'],
                            role=line['role'],
                            bio=line['bio'],
                            first_name=line['first_name'],
                            last_name=line['last_name'],
                        )
        finally:
            file_obj.close()


        # ______________REVIEW______________ НЕ РАБОТАЕ - НУЖЕН USER
        try:
            with open('a:/Dev/api_yamdb/api_yamdb/static/data/review.csv', encoding='utf-8') as file_obj:  # сделать относительный путь к файлу
                reader = csv.DictReader(file_obj, delimiter=',')
                for line in reader:
                    # print(line['id'])
                    # print(line['title_id'])
                    # print(line['text'])
                    # print(line['author'])
                    # print(line['score'])
                    # print(line['pub_date'])

                    title = get_object_or_404(Title, pk=line['title_id'])
                    author = get_object_or_404(User, pk=line['author'])

                    if Review.objects.filter(pk=line['id']).exists():
                        obj = Review.objects.get(pk=line['id'])
                        obj.title = title
                        obj.text = line['text']
                        obj.author = author
                        obj.score = line['score']
                        obj.pub_date = line['pub_date']
                        obj.save()
                    else:
                        Review.objects.create(
                            title=title,
                            text=line['text'],
                            author=author,
                            score=line['score'],
                            pub_date=line['pub_date'],
                        )

        finally:
            file_obj.close()

        # ______________COMMENT______________
        try:
            with open('a:/Dev/api_yamdb/api_yamdb/static/data/comments.csv', encoding='utf-8') as file_obj:  # сделать относительный путь к файлу
                reader = csv.DictReader(file_obj, delimiter=',')
                for line in reader:
                    # print(line['id'])
                    # print(line['review_id'])
                    # print(line['text'])
                    # print(line['author'])
                    # print(line['pub_date'])

                    review = get_object_or_404(Review, pk=line['review_id'])
                    author = get_object_or_404(User, pk=line['author'])

                    if Comment.objects.filter(pk=line['id']).exists():
                        obj = Title.objects.get(pk=line['id'])
                        obj.review = review
                        obj.name = line['text']
                        obj.year = line['author']
                        obj.pub_date = line['pub_date']  # преобразовать в time
                        obj.save()
                    else:
                        Comment.objects.create(
                            review=review,
                            text=line['text'],
                            author=author,
                            pub_date=line['pub_date']
                        )

        finally:
            file_obj.close()

        # ______________GENRE______________
        try:
            with open('a:/Dev/api_yamdb/api_yamdb/static/data/genre.csv', encoding='utf-8') as file_obj:  # сделать относительный путь к файлу
                reader = csv.DictReader(file_obj, delimiter=',')
                for line in reader:
                    # print(line['id'])
                    # print(line['name'])
                    # print(line['slug'])

                    if Genre.objects.filter(pk=line['id']).exists():
                        obj = Genre.objects.get(pk=line['id'])
                        obj.name = line['name']
                        obj.slug = line['slug']
                        obj.save()
                    else:
                        Genre.objects.create(
                            name=line['name'],
                            slug=line['slug']
                        )

        finally:
            file_obj.close()

        # ______________GENRE_TITLE______________
        try:
            with open('a:/Dev/api_yamdb/api_yamdb/static/data/genre_title.csv', encoding='utf-8') as file_obj:  # сделать относительный путь к файлу
                reader = csv.DictReader(file_obj, delimiter=',')
                for line in reader:
                    print(line['id'])
                    print(line['title_id'])
                    print(line['genre_id'])

                    if GenreTitle.objects.filter(pk=line['id']).exists():  # GenreTitle - FAIL!
                        obj = GenreTitle.objects.get(pk=line['id'])
                        obj.name = line['name']
                        obj.slug = line['slug']
                        obj.save()
                    else:
                        Genre.objects.create(
                            name=line['name'],
                            slug=line['slug']
                        )

        finally:
            file_obj.close()




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
