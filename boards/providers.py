from faker.providers import BaseProvider
from django.core.files import File
import random
import os


class ImageProvider(BaseProvider):
    def image(self, path):
        rand_file = random.choice(os.listdir(path))
        return File(open(os.path.join(path, rand_file), 'rb'))
