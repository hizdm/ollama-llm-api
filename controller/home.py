# -*- coding: utf-8 -*-
import sys
from controller.base import BaseHandler

"""
LLM API Frame Home
"""
class IndexHandler(BaseHandler):
    def get(self):
        self.render("home.html", name="LAF", description="A framework for invoking large language models!")