# -*- coding: utf-8 -*-
"""Upgrade from version 004 to version 005."""

import re
from HTMLParser import HTMLParser
from Products.CMFCore.utils import getToolByName


patt = re.compile("\<dt\>Description:\s*\</dt\>\<dd\>(.*?)\</dd\>", re.S)
html_parser = HTMLParser()


class MLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def upgrade(context):
    """Set the Description attribute of ToolExamples based on the main text.
    """
    catalog = getToolByName(context, "portal_catalog")

    brains = catalog(portal_type="osha.campaigntoolkit.toolexample")
    for b in brains:
        obj = b.getObject()
        if obj.description:
            continue
        if obj.text:
            text = obj.text.raw
            match = patt.search(text)
            if match:
                desc = match.group(1)
                desc = strip_tags(desc)
                obj.description = desc
                obj.reindexObject()
