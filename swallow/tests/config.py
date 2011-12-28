import os
import shutil

from . import Article
from integration import ArticleConfig

from swallow.config import DefaultConfig
from swallow.wrappers import XmlWrapper
from swallow.populator import BasePopulator
from swallow.builder import BaseBuilder

from django.test import TestCase
from django.conf import settings

CURRENT_PATH = os.path.dirname(__file__)


class ConfigTests(TestCase):

    def setUp(self):
        settings.SWALLOW_DIRECTORY = os.path.join(CURRENT_PATH, 'import')

        self.import_dir = os.path.join(CURRENT_PATH, 'import')
        if os.path.exists(self.import_dir):
            shutil.rmtree(self.import_dir)
        import_initial = os.path.join(CURRENT_PATH, 'import.initial')
        shutil.copytree(import_initial, self.import_dir)

    def tearDown(self):
        shutil.rmtree(self.import_dir)

    def test_dry_run(self):
        """Test that dryrun doesn't create new instance and
        that input files are not moved"""

        class ArticleBuilder(BaseBuilder):
            pass

        class ArticleConfig(DefaultConfig):

            def builder(self, path, fd):
                return ArticleBuilder(path, fd)

            def instance_is_modified(self, instance):
                return False

        config = ArticleConfig(dryrun=True)
        config.run()

        content = os.listdir(config.input_dir)

        self.assertEqual(3, len(content))
        self.assertIn('ski.xml', content)
        self.assertIn('boxe.xml', content)
        self.assertIn('bilboquet.xml', content)
        self.assertEqual(0, Article.objects.count())

    def test_skip(self):
        """Test that if ``Builder.skip`` returns ``True`` the instance
        creation is skipped"""

        class SkipWrapper(XmlWrapper):
            title = 'foo'

            @property
            def instance_filters(self):
                return {'title': self.item.text}

            @classmethod
            def iter_wrappers(cls, path, f):
                root = super(SkipWrapper, cls).iter_wrappers(path, f)[0]
                for item in root.item.iterfind('item'):
                    yield cls(item, path)

            kind = 'kind'
            title = 'title'
            author = 'author'
            modified_by = 'modified_by'

        class SkipPopulator(BasePopulator):
            _fields_one_to_one = (
                'title',
                'kind',
                'author',
                'modified_by',
            )
            _fields_if_instance_already_exists = []
            _fields_if_instance_modified_from_last_import = []

        class SkipBuilder(BaseBuilder):

            Wrapper = SkipWrapper
            Model = Article
            Populator = SkipPopulator

            def skip(self, wrapper):
                txt = wrapper.item.text
                return txt in ('1', '2')

            def instance_is_modified(self, instance):
                return False

        class SkipConfig(DefaultConfig):

            def builder(self, path, fd):
                return SkipBuilder(path, fd)

            def instance_is_modified(self, instance):
                return False

        config = SkipConfig()
        config.run()

        self.assertEqual(2, Article.objects.count())