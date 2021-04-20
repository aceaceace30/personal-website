from django.test import TestCase
from blogs.models import Blog, Tag, BlogTag


class TestModels(TestCase):
    """Unit test for blogs/models.py"""

    def setUp(self):
        self.blog = Blog.objects.create(title='test title',
                                        slug='test-title',
                                        cover='test-cover.png',
                                        content='test-content')

        self.tag = Tag.objects.create(name='test-tag', color='#FFFFFF')

    def test_blog_str(self):
        """Asserts that str of Blog object returns the value of title field"""
        self.assertEqual('test title', self.blog.__str__())

    def test_tag_str(self):
        """Asserts that str of Tag object returns the value of name field"""
        self.assertEqual('test-tag', self.tag.__str__())

    def test_blog_tag_methods(self):
        """
        Asserts that methods of BlogTag objects is working correctly
        __str__: returns the value of name field in Tag
        color: returns the value of color field in Tag
        name: returns the value of name field in Tag
        """
        self.blog.tags.add(self.tag)
        blog_tag = BlogTag.objects.get(blog__title='test title', tag__name='test-tag')

        self.assertEqual('test-tag', blog_tag.__str__())
        self.assertEqual('#FFFFFF', blog_tag.color)
        self.assertEqual('test-tag', blog_tag.name)
