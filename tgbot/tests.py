import os
import django
import unittest
from unittest import mock
from tgbot.services import process_message
from tgbot.models import Keyword, Specialty

# Установите DJANGO_SETTINGS_MODULE перед выполнением других операций
os.environ['DJANGO_SETTINGS_MODULE'] = 'tgbot.settings'
# Настройка Django
django.setup()


class ProcessMessageTestCase(unittest.TestCase):
    @mock.patch.object(Keyword, 'objects')
    def test_process_message(self, mock_objects):
        # Создаем фейковые данные
        specialty_web = Specialty(name='Web Development')
        specialty_game = Specialty(name='Game Development')
        specialty_software = Specialty(name='Software Development')

        keywords = [
            Keyword(word='python', specialty=specialty_web),
            Keyword(word='django', specialty=specialty_web),
            Keyword(word='c++', specialty=specialty_game),
            Keyword(word='java', specialty=specialty_software)
        ]
        mock_objects.select_related.return_value.all.return_value = keywords

        message_1 = "I love python and django."
        result_1 = process_message(message_1)
        self.assertIn(specialty_web, result_1)

        message_2 = "I enjoy working on c++ for game development."
        result_2 = process_message(message_2)
        self.assertIn(specialty_game, result_2)

        message_3 = "Java is my favorite language for software development."
        result_3 = process_message(message_3)
        self.assertIn(specialty_software, result_3)

        message_4 = "I don't program at all"
        result_4 = process_message(message_4)
        self.assertEqual(len(result_4), 0)


if __name__ == '__main__':
    unittest.main()