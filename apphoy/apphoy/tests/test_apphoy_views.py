from django.test import TestCase, Client

from apphoy.views import redirect_view


class TestViews(TestCase):

    def test_redirect_view(self):
        request = self.client.get('', follow=True)
        response = redirect_view(request)
        response.client = Client()
        self.assertRedirects(response,
                             '/persons/',
                             status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)
