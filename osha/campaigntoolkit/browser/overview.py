from Products.Five.browser import BrowserView


class Overview(BrowserView):
    """Two column overview view."""

    def __call__(self):
        return self.index()

    def two_column_list(self, input_list):
        """Generate a two column list for the provided list. Based on the code
        in plone.app.controlpanel.overview.
        """
        list_len = len(input_list)

        # Calculate the length of the sublists
        sublist_len = (list_len % 2 == 0 and list_len / 2 or list_len / 2 + 1)

        # Calculate the list end point given the list number
        def _list_end(num):
            return (num == 2 and list_len or (num + 1) * sublist_len)

        # Generate only filled columns
        final = []
        for i in range(2):
            column = input_list[i * sublist_len:_list_end(i)]
            if len(column) > 0:
                final.append(column)
        return final

    def sublists(self):
        query = {
            'portal_type': 'Folder',
            'review_state': 'published',
            'sort_on': 'getObjPositionInParent'
        }
        items = self.context.restrictedTraverse('@@folderListing')(**query)
        return self.two_column_list(items)
