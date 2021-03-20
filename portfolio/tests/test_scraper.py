from unittest.mock import patch

from django.test import LiveServerTestCase

from portfolio.scraper import LinkChecker


class LinkCheckerTestCase(LiveServerTestCase):
    """Unit tests for LinkChecker class methods"""
    fixtures = ['portfolio/fixtures/test_views.json']

    def setUp(self) -> None:
        self.link_checker = LinkChecker()

    def test_validate_returns_false(self):
        """
        Test if validate method is returning false for ff cases:
            - url contains the word `www.linkedin.com` and status code is 999
            - status code is equal to 200
        """
        result = self.link_checker.validate('www.linkedin.com/myprofile/test/', 999)
        self.assertFalse(result)

        result = self.link_checker.validate('www.test-site.com/', 200)
        self.assertFalse(result)

    def test_validate_returns_true(self):
        """Test if validate method is returning true for broken url and status code is not equal 200"""
        result = self.link_checker.validate('www.broken-url.com/', 404)
        self.assertTrue(result)

    def test_get_broken_links_valid_broken_url(self):
        href_value = self.live_server_url + '/invalid-path/'
        test_content = bytes(f'<a href="{href_value}">Invalid Site</a>', encoding='utf-8')
        self.link_checker.get_broken_links(test_content)

        self.assertEqual((href_value, 404), self.link_checker.broken_links[0])
        self.assertEqual(f'<ul><li>{href_value} - 404</li>', self.link_checker.html_message)

    def test_get_broken_links_in_exception(self):
        """Test if get_broken_links is not considering the exceptions as broken link"""
        href_value = 'https://www.linkedin.com/in/michael-jay-ababao-3518b0162/'
        test_content = bytes(f'<a href="{href_value}">LinkedIn</a>', encoding='utf-8')
        self.link_checker.get_broken_links(test_content)

        self.assertListEqual([], self.link_checker.broken_links)

    def test_get_broken_links_not_adding_valid_links(self):
        """Test if get_broken_links is not adding non broken links"""
        href_value = self.live_server_url
        test_content = bytes(f'<a href="{href_value}">Valid Url</a>', encoding='utf-8')
        self.link_checker.get_broken_links(test_content)

        self.assertListEqual([], self.link_checker.broken_links)

    def test_get_site_urls(self):
        """Test if get_site_urls is returning list of site links"""
        expected_result = ['http://127.0.0.1:8000/',
                           'http://127.0.0.1:8000/portfolio/project/qoute-generator/',
                           'http://127.0.0.1:8000/portfolio/project/inventory-management-system/']
        site_urls = self.link_checker.get_site_urls()
        self.assertEqual(expected_result, site_urls)

    @patch.object(LinkChecker, 'get_broken_links')
    @patch('portfolio.scraper.requests.get')
    def test_run(self, mock_req_get, mock_get_broken_links):
        """Test the following if the mocked objects are called"""
        self.link_checker.run()

        self.assertEqual(3, mock_req_get.call_count)
        self.assertEqual(3, mock_get_broken_links.call_count)
