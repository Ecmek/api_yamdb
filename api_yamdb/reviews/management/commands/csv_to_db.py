import csv
import sqlite3
from django.shortcuts import get_object_or_404
from django.core.management.base import BaseCommand  # , CommandError
from reviews.models import Category, Comment, Genre, Review, Title, User
from api_yamdb.settings import CSV_DATA_DIR


def transfer_comments(line):
    review = get_object_or_404(Review, pk=line['review_id'])
    author = get_object_or_404(User, pk=line['author'])

    if Comment.objects.filter(pk=line['id']).exists():
        obj = Title.objects.get(pk=line['id'])
        obj.review = review
        obj.name = line['text']
        obj.year = line['author']
        obj.pub_date = line['pub_date']
        obj.save()
    else:
        Comment.objects.create(
            review=review,
            text=line['text'],
            author=author,
            pub_date=line['pub_date']
        )


def transfer_review(line):
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


def transfer_users(line):
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


def transfer_titles(line):
    category = get_object_or_404(Category, pk=line['category'])

    if Title.objects.filter(pk=line['id']).exists():
        obj = Title.objects.get(pk=line['id'])
        obj.name = line['name']
        obj.year = line['year']
        obj.category = category
        obj.save()
    else:
        Title.objects.create(
            name=line['name'],
            year=line['year'],
            category=category
        )


def transfer_genre(line):
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


def transfer_category(line):
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


def transfer_genre_title():
    """Переносит данные из static/data/genre_title.csv в базу данных.
    """
    try:
        print('Перенос из genre_title.csv - Старт')
        sqlite_connection = sqlite3.connect(
            'a:/Dev/api_yamdb/api_yamdb/db.sqlite3'
        )
        cursor = sqlite_connection.cursor()

        with open(
            CSV_DATA_DIR + 'genre_title.csv', encoding='utf-8'
        ) as file_obj:

            reader = csv.DictReader(file_obj, delimiter=',')

            for line in reader:
                sql_select_query = (
                    """SELECT * FROM reviews_title_genre WHERE id = ?"""
                )
                info = cursor.execute(sql_select_query, (line['id'],))

                # если запись с id есть в БД, перезаписываем:
                if info.fetchone() is not None:
                    record_list = (
                        line['title_id'], line['genre_id'], line['id']
                    )
                    sqlite_update_query = """Update reviews_title_genre
                        SET title_id = ?, genre_id = ? WHERE id = ?"""
                    cursor.execute(sqlite_update_query, record_list)
                    sqlite_connection.commit()

                else:  # если записи нет, то создаём:
                    sqlite_insert_with_param = """INSERT INTO reviews_title_genre
                                               (title_id, genre_id)
                                               VALUES (?, ?);"""
                    data_tuple = (line['title_id'], line['genre_id'])
                    cursor.execute(sqlite_insert_with_param, data_tuple)
                    sqlite_connection.commit()

            print('Перенос из genre_title.csv - Готово')

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if sqlite_connection:
            sqlite_connection.close()

        file_obj.close()


FUNCTIONS = [
    {
        'file_name': 'category',
        'function': transfer_category
    },
    {
        'file_name': 'genre',
        'function': transfer_genre
    },
    {
        'file_name': 'titles',
        'function': transfer_titles
    },
    {
        'file_name': 'users',
        'function': transfer_users
    },
    {
        'file_name': 'review',
        'function': transfer_review
    },
    {
        'file_name': 'comments',
        'function': transfer_comments
    },
]


class Command(BaseCommand):
    help = 'Переносит данные из файлов .csv в базу данных'  # Александр Иванов: "желательно, чтобы ревьюер смог воспроизвести БД :slightly_smiling_face:"

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
        for function in FUNCTIONS:
            try:
                file_name = function.get('file_name')
                function = function.get('function')

                print('Перенос из ', file_name, '.csv - Старт')

                with open(
                    CSV_DATA_DIR + file_name + '.csv', encoding='utf-8'
                ) as file_obj:

                    reader = csv.DictReader(file_obj, delimiter=',')
                    for line in reader:
                        function(line)

                    print('Перенос из ', file_name, '.csv - Готово')
            finally:
                file_obj.close()

        # # ______________CATEGORY______________
        # try:
        #     print('Перенос из category.csv - Старт')
        #     with open(CSV_DATA_DIR + 'category.csv', encoding='utf-8') as file_obj:
        #         reader = csv.DictReader(file_obj, delimiter=',')
        #         for line in reader:
        #             transfer_category(line)

        #         print('Перенос из category.csv - Готово')
        # finally:
        #     file_obj.close()

        # # ______________GENRE______________
        # try:
        #     print('Перенос из genre.csv - Старт')
        #     with open(CSV_DATA_DIR + 'genre.csv', encoding='utf-8') as file_obj:
        #         reader = csv.DictReader(file_obj, delimiter=',')
        #         for line in reader:
        #             transfer_genre(line)

        #         print('Перенос из genre.csv - Готово')

        # finally:
        #     file_obj.close()

        # # ______________TITLE______________
        # try:
        #     print('Перенос из titles.csv - Старт')
        #     with open(CSV_DATA_DIR + 'titles.csv', encoding='utf-8') as file_obj:
        #         reader = csv.DictReader(file_obj, delimiter=',')
        #         for line in reader:
        #             transfer_title(line)

        #         print('Перенос из titles.csv - Готово')
        # finally:
        #     file_obj.close()

        # # ______________USER______________
        # try:
        #     print('Перенос из users.csv - Старт')
        #     with open(CSV_DATA_DIR + 'users.csv', encoding='utf-8') as file_obj:
        #         reader = csv.DictReader(file_obj, delimiter=',')
        #         for line in reader:
        #             transfer_user(line)

        #         print('Перенос из users.csv - Готово')
        # finally:
        #     file_obj.close()

        # # ______________REVIEW______________
        # try:
        #     print('Перенос из review.csv - Старт')
        #     with open(CSV_DATA_DIR + 'review.csv', encoding='utf-8') as file_obj:
        #         reader = csv.DictReader(file_obj, delimiter=',')
        #         for line in reader:
        #             transfer_review(line)

        #         print('Перенос из review.csv - Готово')

        # finally:
        #     file_obj.close()

        # # ______________COMMENT______________
        # try:
        #     print('Перенос из comment.csv - Старт')
        #     with open(CSV_DATA_DIR + 'comments.csv', encoding='utf-8') as file_obj:
        #         reader = csv.DictReader(file_obj, delimiter=',')
        #         for line in reader:
        #             transfer_comment(line)

        #         print('Перенос из comment.csv - Готово')

        # finally:
        #     file_obj.close()

        transfer_genre_title()


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
