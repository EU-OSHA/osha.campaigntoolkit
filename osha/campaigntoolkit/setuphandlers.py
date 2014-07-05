from plone import api
import logging

log = logging.getLogger(__name__)


def _setup_password_policy(context=None):
    acl_users = api.portal.get_tool('acl_users')
    if not acl_users.objectIds('Password Strength Plugin'):
        setup = api.portal.get_tool('portal_setup')
        setup.runAllImportStepsFromProfile(
            'profile-Products.PasswordStrength:default')
        plugin = acl_users.get('password_strength_plugin')
        log.info('Password Strength Plugin created')
    else:
        plugin = acl_users.get(
            acl_users.objectIds('Password Strength Plugin')[0])
        log.info('Using existing Password Strength Plugin')
    plugin.p1_re = '.{8}.*'
    plugin.p1_err = 'Minimum 8 characters.'
    plugin.p2_re = '.*[A-Z].*'
    plugin.p2_err = 'Minimum 1 capital letter.'
    plugin.p3_re = '.*[a-z].*'
    plugin.p3_err = 'Minimum 1 lower case letter.'
    plugin.p4_re = '.*[0-9].*'
    plugin.p4_err = 'Minimum 1 number.'
    plugin.p5_re = '.*[^0-9a-zA-Z ].*'
    plugin.p5_err = 'Minimum 1 non-alpha character.'
    log.info('Password Strength policy set')


def setup_password_policy(context):
    if context.readDataFile('osha.campaigntoolkit.marker.txt') is None:
        return
    _setup_password_policy()
