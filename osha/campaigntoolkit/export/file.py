
# -*- coding: utf-8 -*-

from . import base
from Acquisition import aq_parent
from ordereddict import OrderedDict


FILE_PATHS = [
    "{0}/about",
    "{0}/how-to-run-a-campaign",
    "{0}/tools",
]


class FileExporter(base.BaseExporter):
    name = 'files'

    fields = OrderedDict([
        ('title', base.handleString),
        ('description', base.handleText),
        ('file', base.handlePrimaryFileField),
        ('subject', base.handleList),
    ])
    base_query = dict(portal_type='File')

    def set_up_parameters(self, context):
        super(FileExporter, self).set_up_parameters(context)
        self.search_parameters['sort'] = 'Date desc'
        self.filter_paths = [
            path.format(self.PORTAL_PATH) for path in FILE_PATHS]
        self.query = self.base_query

    def skip_result(self, brain, obj=None):
        item_path = brain.getPath()
        # filter out content under paths not explicitly supported
        for path in self.filter_paths:
            if item_path.startswith(path):
                return False
        base.log.info('Skip due to wrong path: {0}'.format(item_path))
        return True
