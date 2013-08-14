from plone import api
import logging

logger = logging.getLogger('osha.policy.upgrades')


def upgrade(context):
    qi = api.portal.get_tool("portal_quickinstaller")
    
    for product in ("LoginLockout", "PasswordStrength"):
        if not qi.isProductInstalled(product):
            logger.info("Installing Products.%s" % product)
            qi.installProduct(product)

    au = api.portal.get_tool("acl_users")
    ps_plugin = au.password_strength_plugin
    ps_plugin.manage_changeProperties(p1_re=".{8}.*", p1_err="Minimum 8 characters.")
            
    logger.info("PasswordStrength configured.")
