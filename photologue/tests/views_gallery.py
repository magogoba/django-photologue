#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from photologue.tests.factories import GalleryFactory
from django.test import TestCase

YEAR = datetime.now().year
MONTH = datetime.now().ctime().split(' ')[1].lower()
DAY = datetime.now().day

class RequestGalleryTest(TestCase):

    urls = 'photologue.tests.test_urls'

    def setUp(self):
        super(RequestGalleryTest, self).setUp()
        self.gallery = GalleryFactory(title_slug='test-gallery')

    def test_archive_gallery_url_works(self):
        response = self.client.get('/ptests/gallery/')
        self.assertEqual(response.status_code, 200)

    def test_archive_gallery_empty(self):
        """If there are no galleries to show, tell the visitor - don't show a
        404."""

        self.gallery.is_public = False
        self.gallery.save()

        response = self.client.get('/ptests/gallery/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['latest'].count(),
                         0)

    def test_paginated_gallery_url_works(self):
        response = self.client.get('/ptests/gallery/page/1/')
        self.assertEqual(response.status_code, 200)

    def test_gallery_works(self):
        response = self.client.get('/ptests/gallery/test-gallery/')
        self.assertEqual(response.status_code, 200)

    def test_archive_year_gallery_works(self):
        response = self.client.get('/ptests/gallery/{0}/'.format(YEAR))
        self.assertEqual(response.status_code, 200)

    def test_archive_month_gallery_works(self):
        response = self.client.get('/ptests/gallery/{0}/{1}/'.format(YEAR, MONTH))
        self.assertEqual(response.status_code, 200)

    def test_archive_day_gallery_works(self):
        response = self.client.get('/ptests/gallery/{0}/{1}/{2}/'.format(YEAR, MONTH, DAY))
        self.assertEqual(response.status_code, 200)

    def test_detail_gallery_works(self):
        response = self.client.get('/ptests/gallery/{0}/{1}/{2}/test-gallery/'.format(YEAR, MONTH, DAY))
        self.assertEqual(response.status_code, 200)

    def test_redirect_to_list(self):
        """Trivial test - if someone requests the root url of the app
        (i.e. /ptests/'), redirect them to the gallery list page."""
        response = self.client.get('/ptests/')
        self.assertRedirects(response, '/ptests/gallery/', 301, 200)


