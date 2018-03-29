from Acquisition import aq_parent
from datetime import datetime
from OFS.Image import Pdata
from plone import api
from plone.dexterity.interfaces import IDexterityContent
from plone.i18n.normalizer.interfaces import IUserPreferredFileNameNormalizer
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import isDefaultPage
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from StringIO import StringIO
from ZODB.POSException import POSKeyError
from zope import component
from zope.component import queryUtility
from zope.component.hooks import getSite
import re


from plone.app.uuid.utils import uuidToURL
from plone.app.uuid.utils import uuidToObject

from lxml import etree

import csv
import logging
import os
import tempfile

log = logging.getLogger(__name__)

uid_patt = re.compile("""["'](\./)*(http://|https://)*resolveuid/(.*?)(/image_preview)*(/image)*[/'"]""")
img_patt = re.compile("""src=["'](.*?)/image(_*.*?)["']""")

ESCAPECHAR = '<@#&>'
LIST_ESCAPECHAR = '<&#@>'
DEFAULT_PORTAL_PATH = '/Plone'
DEFAULT_SITE_URL = "http://toolkit.osha.europa.eu/"
DEFAULT_SITE_URL_HTTP = "http://toolkit.osha.europa.eu/"
DEFAULT_SERVER_URL = DEFAULT_SITE_URL
# LEN_PORTAL_PATH = len(PORTAL_PATH.split('/'))

NSMAP = {None: "http://fake.domain/gfb/1.0"}

csv.register_dialect(
    'bilbomatica', delimiter=';', doublequote=False,
    quoting=csv.QUOTE_ALL,
)


def handleString(context, value, obj=None):
    # bbb
    # We actually don't need to make a difference between text and string
    return handleText(context, value, obj)


def handleBool(context, value, obj=None):
    if value:
        return "1"
    return "0"


def handleInt(context, value, obj=None):
    value = str(value)
    return handleString(context, value, obj)


def handleRichText(context, value, obj=None):
    return handleText(context, value.raw, obj)


def handleText(context, value, obj=None, replace_portal_path=True):
    value = safe_unicode(value).strip() #.replace('"', ESCAPECHAR)
    value = value.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

    def replace_uuid(match):
        value = match.group()
        uuid = match.group(3)
        if not uuid:
            return value
        item = uuidToObject(uuid)
        if not item:
            return value
        return u'"{0}"'.format(uuidToURL(uuid))

    def replace_img(match):
        return u'src="{0}"'.format(match.group(1))

    if "resolveuid" in value:
        value = uid_patt.sub(replace_uuid, value)
    if "image" in value:
        value = img_patt.sub(replace_img, value)
    if replace_portal_path:
        value = value.replace('{0}{1}'.format(context.SERVER_URL, context.PORTAL_PATH[1:]), '')
        value = value.replace(context.SITE_URL, '/').replace(context.SITE_URL_HTTP, '/')
    return value


def handleTextList(context, value, obj=None):
    text = u"<br/>".join([safe_unicode(x).strip() for x in value])
    return u"<p>{0}</p>".format(text)


def handleList(context, value, obj=None):
    return ", ".join([safe_unicode(x) for x in value])


def handleMultilingualThesaurus(context, value, obj=None):
    vocab = api.portal.get_tool("portal_vocabularies").get('MultilingualThesaurus')
    filtered_value = [i for i in value if vocab.getTermByKey(i)]
    return handleList(context, filtered_value, obj)


def handleNACE(context, value, obj=None):
    vocab = api.portal.get_tool("portal_vocabularies").get('NACE')
    filtered_value = [i for i in value if vocab.getTermByKey(i)]
    return handleList(context, filtered_value, obj)


def handleRiskfactors(context, value, obj=None):
    vocab = api.portal.get_tool("portal_vocabularies").get('RiskFactors')
    filtered_value = [i for i in value if vocab.getTermByKey(i)]
    friendly_value = [vocab.getTermByKey(i) for i in filtered_value]
    return handleList(context, friendly_value, obj)


def handleType_methodology(context, value, obj=None):
    vocab = api.portal.get_tool("portal_vocabularies").get('RiskassessmentTypeMethodology')
    filtered_value = [i for i in value if vocab.getTermByKey(i)]
    friendly_value = [vocab.getTermByKey(i) for i in filtered_value]
    return handleList(context, friendly_value, obj)


def handleProviderCategory(context, value, obj=None):
    vocab = api.portal.get_tool("portal_vocabularies").get('provider_category')
    filtered_value = [i for i in value if vocab.getTermByKey(i)]
    friendly_value = [vocab.getTermByKey(i) for i in filtered_value]
    return handleList(context, friendly_value, obj)


def handleAdditionalKeywords(context, value, obj=None):
    return handleList(context, [x.get('Keywords') for x in value], obj)


def handleDate(context, value, obj=None):
    if value is not None:
        return value.strftime('%Y-%m-%d %H:%M:%S')
    return ""


def handlePrimaryFileField(context, value, obj=None):
    return handleFileField(context, value, obj, is_primary=True)


def handleRelatedItems(context, value, obj=None):
    if value:
        paths = []
        for item in value:
            if item.portal_type in ['File', 'Image']:
                fieldval = item.getPrimaryField().getAccessor(item)()
                paths.append(handleFileField(
                    context, fieldval, item, is_primary=True))
        return handleList(context, paths)
    return ""


def handleProvider(context, value, obj=None):
    if value:
        provider = value[0]
        return "/".join(provider.getPhysicalPath()).replace(context.PORTAL_PATH, '')
    return ""


def handleFileField(context, value, obj=None, is_primary=False, with_title=False):
    if not value:
        return ""
    name = getattr(value, 'filename', '')
    # if obj:
    #     name = obj.getId()
    # if not name:
    #     try:
    #         name = value.getId()
    #     except:
    #         name = ''
    # if not name:
    #     return ''
    name = IUserPreferredFileNameNormalizer(context.request).normalize(
        safe_unicode(name))
    # Crude band-aid: if there's no ending, stick in the lower part of
    # the content type
    if name.find('.') == -1:
        if IDexterityContent.providedBy(obj):
            content_type = getattr(value, 'contentType', '')
        else:
            content_type = getattr(value, 'content_type', '')
        name = "{0}.{1}".format(
            name, content_type.split('/')[-1])
    if is_primary:
        item_path = '/'.join(aq_parent(obj).getPhysicalPath()[context.LEN_PORTAL_PATH:])
    else:
        item_path = '/'.join(obj.getPhysicalPath()[context.LEN_PORTAL_PATH:])
    file_path = '/{0}/{1}'.format(item_path, name)
    try:
        data = value.data
    except POSKeyError:
        data = ""
    if isinstance(data, Pdata):
        data = data.data
    if len(data) == 0:
        return ''
    if context.export_binary:
        os.chdir(context.exportdir)
        if not os.path.exists(item_path):
            os.makedirs(item_path)
        fn = '{0}{1}'.format(context.exportdir, file_path)
        try:
            fh = open(fn, 'w')
        except IOError, err:
            if err.strerror == 'File name too long':
                # try to build a shorter filename
                name = "{0}.{1}".format(obj.id, value.content_type.split('/')[-1])
                file_path = '/{0}/{1}'.format(item_path, name)
                fn = '{0}{1}'.format(context.exportdir, file_path)
                try:
                    fh = open(fn, 'w')
                except IOError:
                    fh = None
                    file_path = ''
            else:
                fh = None
                file_path = ''
        except Exception:
            fh = None
            file_path = ''
        if fh:
            fh.write(data)
    if with_title:
        return "{0}|{1}".format(obj.Title(), file_path)
    else:
        return file_path



class BaseExporter(BrowserView):
    """Exports content into csv """

    query = ''
    # limit number of results, useful for testing
    limit = 1000
    search_parameters = {}
    metadata_fields = [
        'path', 'language', 'workflow_state', 'creation_date',
        'modification_date', 'publication_date', 'expiration_date', 'creator',
        # 'archived', 'is_default_page', 'aliases',
    ]
    # Schema fields, handled by content accessor
    fields = []
    # additional fields, handled be custom methods
    extra_fields = []
    name = 'generic'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.SERVER_URL = self.request.SERVER_URL + '/'
        self.PORTAL_PATH = DEFAULT_PORTAL_PATH
        self.LEN_PORTAL_PATH = len(self.PORTAL_PATH.split('/'))
        self.SITE_URL = DEFAULT_SITE_URL
        self.SITE_URL_HTTP = DEFAULT_SITE_URL_HTTP

    def __call__(self):
        context = self.context
        portal = api.portal.get()
        self.start = datetime.now()
        self.pwt = getToolByName(portal, 'portal_workflow')
        self.plt = getToolByName(portal, 'portal_languages')
        self.catalog = getToolByName(portal, 'portal_catalog')
        self.languages = self.plt.getSupportedLanguages()
        self.props = portal.portal_properties

        if 'limit' in self.request:
            try:
                self.limit = int(self.request.get('limit', ''))
            except:
                # ignore, use hard-coded limit
                pass

        self.export_binary = 'export_binary' in self.request
        exportdir = self.request.get('exportdir', '')
        if exportdir and os.path.exists(exportdir) and os.access(exportdir, os.W_OK):
            self.exportdir = exportdir
        else:
            self.exportdir = tempfile.mkdtemp()

        # Hook
        self.set_up_parameters(context)

        if 'stats' in self.request:
            return self.export_statistics()
        if not self.export_binary:
            response = self.request.RESPONSE
            self.set_response_headers(response)
        return self.export_data()

    def set_up_parameters(self, context):
        """ Provide hook for intial setup,
        extend in the content-type based classes """
        self.search_parameters['rows'] = self.limit
        self.search_parameters['start'] = 0

    def skip_result(self, brain, obj=None):
        return False

    def export_data(self):

        # fieldnames = self.metadata_fields + self.fields.keys() + self.extra_fields
        # buffer = StringIO()
        # writer = csv.DictWriter(
        #     buffer,
        #     fieldnames=fieldnames,
        #     dialect='bilbomatica')

        output = etree.Element(self.name, nsmap=NSMAP)

        query = self.query
        # if "Language" not in query:
        #     query = ' ' .join((
        #         query, "AND +Language:(any OR {0})".format(' OR '.join(self.languages)),
        #     ))
        log.info('query: {0}'.format(query))

        results = self.catalog(**query)
        log.info('Number of results found: {0}'.format(len(results)))

        # results = cat(query)
        # if len(results):
        #     writer.writerow(dict((fn, fn) for fn in fieldnames))
        nrows = 0
        by_language = {}
        for res in results:
            try:
                obj = res.getObject()
            except:
                log.warn("Could not get object for {0}".format(res.getPath()))
                continue
            if obj is None:
                log.warn("Could not get object for {0}. Stale catalog entry?".format(res.getPath()))
            if self.skip_result(res, obj):
                continue
            node = etree.SubElement(output, 'item')
            data = self.get_metadata(obj)
            for fn, func in self.fields.items():
                if IDexterityContent.providedBy(obj):
                    value = getattr(obj, fn, None)
                else:
                    value = obj.getField(fn).getAccessor(obj)()
                data[fn] = func(self, value, obj)
                # rendered_value = func(self, value, obj)
            # XXX export contained contents
            data = self.export_contained_contents(data, obj)
            nrows += 1
            # writer.writerow(data)
            for fn, value in data.items():
                etree.SubElement(node, fn).text = value
            # write stats
            lang = obj.Language()
            if lang in by_language:
                by_language[lang] += 1
            else:
                by_language[lang] = 1
            if nrows >= self.limit:
                break

        # csv_data = buffer.getvalue()
        # buffer.close()
        xml_data = etree.tostring(
            output, pretty_print=True, xml_declaration=True, encoding="utf-8")

        stats = "Set limit was: {limit}.\nTotal number of type '{item}' is: " \
            "{total}.\nBy language: {by_language}".format(
                item=self.name, total=nrows, by_language=by_language, limit=self.limit)

        if self.export_binary:
            fn = '{0}/{1}.xml'.format(self.exportdir, self.name)
            fh = open(fn, 'w')
            fh.write(xml_data)
            fh.close()
            status = "{0}, including binary data, has been exported to {1}".format(
                self.name, self.exportdir)
            return_value = "{0}\n{1}".format(status, stats)
        else:
            return_value = xml_data
            status = "{0} has been exported.".format(self.name)

        log.info('Finished with export after {0} seconds'.format((
            datetime.now() - self.start).seconds))
        log.info(status)
        log.info(stats)
        return return_value

    def export_statistics(self):
        query = self.query

        log.info('query: \n{0}\nparmeters: \n{1}'.format(query, self.search_parameters))
        results = self.catalog(**query)

        by_language = {}
        total = 0
        for res in results:
            if self.skip_result(res):
                continue
            total += 1
            lang = res.Language
            if lang in by_language:
                by_language[lang] += 1
            else:
                by_language[lang] = 1
            if total >= self.limit:
                break

        stats = "Set limit was: {limit}.\nTotal number of type '{item}' is: " \
            "{total}.\nBy language: {by_language}".format(
                item=self.name, total=total, by_language=by_language, limit=self.limit)
        return stats

    def get_metadata(self, obj):
        data = {}
        data['path'] = '/'.join(obj.getPhysicalPath()).replace(self.PORTAL_PATH, '')
        language = obj.Language()
        data['language'] = language
        if self.pwt.getWorkflowsFor(obj) in (None, []):
            state = "n/a"
        else:
            state = self.pwt.getInfoFor(obj, 'review_state')
        data['workflow_state'] = state
        data['creation_date'] = handleDate(self, obj.created())
        data['modification_date'] = handleDate(self, obj.modified())
        data['publication_date'] = handleDate(self, obj.getEffectiveDate())
        data['expiration_date'] = handleDate(self, obj.getExpirationDate())
        # data['archived'] = handleBool(self, IAnnotations(obj).get('slc.outdated', False))
        # data['is_default_page'] = handleBool(self, isDefaultPage(obj, self.request))
        # Only export the first creator
        creators = obj.Creators()
        data['creator'] = handleString(self, len(creators) and creators[0] or '')
        # aliases_view = component.getMultiAdapter((obj, self.request), name='manage-aliases')
        # if aliases_view:
        #     data['aliases'] = handleList(self, [x['path'] for x in aliases_view.redirects()])
        return data

    def set_response_headers(self, response):
        response.setHeader(
            "Content-Disposition",
            "attachment; filename={0}.xml".format(self.name),
        )
        response.setHeader(
            "Content-Type", 'text/xml;charset=utf-8')

    def export_contained_contents(self, data, obj):
        return data

