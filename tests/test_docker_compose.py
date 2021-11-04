import os
import re

from django.conf import settings


class TestDockerfile:

    def test_dockerfile(self):
        try:
            with open(f'{os.path.join(settings.BASE_DIR, "docker-compose.yaml")}', 'r') as f:
                docker_compose = f.read()
        except FileNotFoundError:
            assert False, 'Проверьте, что добавили файл docker-compose.yaml'

        assert re.search(r'image:\s+postgres:', docker_compose), (
            'Проверьте, что добавили образ postgres:latest в файл docker-compose'
        )
        assert re.search(r'build:\s+\.', docker_compose), (
            'Проверьте, что добавили сборку контейнера из Dockerfile в файл docker-compose'
        )
