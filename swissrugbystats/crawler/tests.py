from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO

# deprecated..
#class CrawlerTestCase(TestCase):
    """
    Todo: document.
    Test if the command is callable and returns the right result.
    https://docs.djangoproject.com/en/1.8/topics/testing/tools/#topics-testing-management-commands
    """
    """
    def test_command_output(self):
        out = StringIO()
        call_command('crawl_and_update.py', stdout=out)
        self.assertIn('blubb', out.getvalue())
    """
