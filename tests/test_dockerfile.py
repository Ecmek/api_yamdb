import os
import re

from django.conf import settings


class TestDockerfile:

    def test_dockerfile(self):
        try:
            with open(f'{os.path.join(settings.BASE_DIR, "Dockerfile")}', 'r') as f:
                dockerfile = f.read()
        except FileNotFoundError:
            assert False, 'Проверьте, что добавили файл Dockerfile'

        assert re.search(r'FROM\s+python:', dockerfile), (
            'Проверьте, что добавили инструкцию FROM с указанием образа python в файл Dockerfile'
        )
        assert re.search(r'((RUN)|(&&))\s+pip(3|)\s+install\s+-r.+requirements\.txt', dockerfile), (
            'Проверьте, что добавили инструкцию RUN с установкой зависимостей из файла '
            'requirements.txt в файл Dockerfile'
        )
        assert re.search(r'CMD\s+gunicorn\s+api_yamdb\.wsgi:application.+$', dockerfile), (
            'Проверьте, что добавили инструкцию CMD с запуском gunicorn в файл Dockerfile'
        )
