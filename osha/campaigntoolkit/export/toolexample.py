# -*- coding: utf-8 -*-

from . import base
from ordereddict import OrderedDict


DOCUMENT_PATHS = [
    "{0}/about",
    "{0}/how-to-run-a-campaign",
    "{0}/tools",
    "{0}/front-page",
]


class ToolexampleExporter(base.BaseExporter):
    name = 'tool_examples'

    fields = OrderedDict([
        ('title', base.handleString),
        ('description', base.handleText),
        ('text', base.handleRichText),
        ('image', base.handlePrimaryFileField),
        ('OSH_related', base.handleBool),
        ('relatedItems', base.handleRelatedItems),
        ('subject', base.handleList),
    ])
    base_query = dict(portal_type="osha.campaigntoolkit.toolexample")

    def set_up_parameters(self, context):
        super(ToolexampleExporter, self).set_up_parameters(context)
        self.search_parameters['sort'] = 'Date desc'
        self.filter_paths = [
            path.format(self.PORTAL_PATH) for path in DOCUMENT_PATHS]

        self.query = self.base_query

    def skip_result(self, brain, obj=None):
        item_path = brain.getPath()

        for path in self.filter_paths:
            if item_path.startswith(path):
                return False
        base.log.info('Skip due to wrong path: {0}'.format(item_path))
        return True
