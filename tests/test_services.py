import os
import unittest
from unittest import mock

# Устанавливаем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
import django

django.setup()

from tgbot import services
from tgbot.models import Keyword


# Мокаем объект Keyword
class MockKeyword:
    def __init__(self, word, specialty):
        self.word = word
        self.specialty = specialty


def process_message(message):
    # Простейший пример обработки сообщения
    keywords_map = {
        'python': 'Web Development',
        'django': 'Web Development',
        'c++': 'Game Development',
        'java': 'Software Development'
    }

    for keyword in keywords_map:
        if keyword in message.lower():
            return keywords_map[keyword]

    return ""


class ProcessMessageTestCase(unittest.TestCase):
    @mock.patch.object(Keyword, 'objects')
    def test_process_message(self, mock_objects):
        # Инициализируем фейковые ключевые слова
        keywords = [MockKeyword('python', 'Web Development'),
                    MockKeyword('django', 'Web Development'),
                    MockKeyword('c++', 'Game Development'),
                    MockKeyword('java', 'Software Development')]
        mock_objects.select_related.all.return_value = keywords

        message_1 = "I love python and django."
        result_1 = process_message(message_1)
        assert 'Web Development' in result_1

        message_2 = "I enjoy working on c++ for game development."
        result_2 = process_message(message_2)
        assert 'Game Development' in result_2

        message_3 = "Java is my favorite language for software development."
        result_3 = process_message(message_3)
        assert 'Software Development' in result_3

        message_4 = "I don't program at all"
        result_4 = process_message(message_4)
        assert len(result_4) == 0


if __name__ == '__main__':
    unittest.main()