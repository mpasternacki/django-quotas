from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

def __user_get_quota(user, base):
    """Return user's quota for `base'.

    Returns True if unlimited, integer if limited, None if no quota was set."""
    def __has_quota_of(limit):
        return user.has_perm( 'quotas.quota_%s_%s'%(base, limit) )
    if __has_quota_of('unlimited'): return True
    try:
        for v in sorted( settings.QUOTAS[base], reverse=True ):
            if __has_quota_of(v):
                return v
    except KeyError: pass               # no base quota
    except AttributeError: pass         # no settings.QUOTAS
    return None

User.add_to_class('get_quota', __user_get_quota)

