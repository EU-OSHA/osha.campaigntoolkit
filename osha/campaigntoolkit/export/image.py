# -*- coding: utf-8 -*-

from . import base
from ordereddict import OrderedDict


FILE_PATHS = [
    "{0}/about",
    "{0}/how-to-run-a-campaign",
    "{0}/tools",
]


class ImageExporter(base.BaseExporter):
    name = 'images'

    fields = OrderedDict([
        ('title', base.handleString),
        ('description', base.handleText),
        ('image', base.handlePrimaryFileField),
        ('subject', base.handleList),
    ])
    base_query = dict(portal_type='Image')

    def set_up_parameters(self, context):
        super(ImageExporter, self).set_up_parameters(context)
        self.filter_paths = [
            path.format(self.PORTAL_PATH) for path in FILE_PATHS]
        self.query = self.base_query

    def skip_result(self, brain, obj=None):
        # filter out content under paths not explicitly supported
        item_path = brain.getPath()

        for path in self.filter_paths:
            if item_path.startswith(path):
                return False
        base.log.info('Skip due to wrong path: {0}'.format(item_path))
        return True
