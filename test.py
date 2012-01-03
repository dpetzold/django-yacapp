#!/usr/bin/env python2.7

from __future__ import print_function

import os
import site
import sys

root = '/home/derrickpetzold/'
sys.path.append(root)
site.addsitedir(root + 'lib/python2.7/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'derrickpetzold.settings'

import argparse
import json
import random
import re
import tempfile
import time

from baku import progress
from baku import stream
from baku import temp
from baku import util
from baku import string_util
from baku.test import base
from baku.test import formatter

from derrickpetzold import settings
from derrickpetzold import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.webdesign import lorem_ipsum as lorem

class TestSite(base.TestBase):

    cookie_path = settings.SITE_ROOT + '/../tmp/cookies-session.jar'

    def __init__(self, **kwargs):
        # login
        super(TestSite, self).__init__(**kwargs)

    def test_login(self):
        response = self.retrieve(
                self.host + 'login/',
                username='testuser',
                password='1userFoo')
        assert response.success == True, 'Login failed: %s' % (response.error)
        self.output.writeln('Login: Ok (%.2f)' % (response.run_time))

    def test_logout(self):
        response = self.retrieve(self.host + 'logout/')
        assert response.success == True, 'Logout failed: %s' % (response.error)
        self.output.writeln('Logout: Ok (%.2f)' % (response.run_time))

    def test_status(self):
        response = self.retrieve(self.host + 'status/')
        assert response.success == True, 'Status failed: %s' % (response.error)
        self.output.writeln('Status: Ok (%.2f)' % (response.run_time))

    def test_post(self):
        response = self.retrieve(
                self.host + 'comment/post/',
                object_pk=17,
                content_type='derrickpetzold.Post',
                csrfmiddlewaretoken=self.csrf(self.host + 'login/'),
                title=lorem.words(random.randint(3, 6), common=False),
                text=lorem.paragraph())

        assert response.success == True, 'Post failed: %s' % (response.error)
        self.output.writeln('Post: Ok (%.2f)' % (response.run_time))

def main():

    TestSite(
        settings=settings,
        formatter=formatter.YamlFormatter()).run()

if __name__ == '__main__':
    main()
