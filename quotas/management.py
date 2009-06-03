from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import signals

import models
# based on http://www.djangosnippets.org/snippets/334/

def ensure_permissions(app, verbosity=0, **kwargs):
    appname = app.__name__.lower().split('.')[-2]

    # create a content type for the app
    ct, created = ContentType.objects.get_or_create(model='', app_label=appname,
                                                    defaults={'name': appname})
    if created and verbosity >= 2: print "Adding custom content type '%s'" % ct

    for base, vv in getattr(settings, 'QUOTAS', {}).items():
        for i in vv:
            p, created = Permission.objects.get_or_create(
                codename='quota_%s_%d' % (base, i),
                content_type__pk = ct.id,
                defaults={'name': '%s quota of %d' % (base, i),
                         'content_type': ct})
            if created and verbosity>=1: print 'Added permission %s' % p
        p, created = Permission.objects.get_or_create(
            codename='quota_%s_unlimited' % base,
            content_type__pk = ct.id,
            defaults={'name': '%s unlimited quota' % base,
                     'content_type': ct})
        if created and verbosity>=1: print 'Added permission %s' % p
    
signals.post_syncdb.connect(ensure_permissions, sender=models)
