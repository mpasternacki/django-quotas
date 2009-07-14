from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from quotas import INFINITY

QUOTAS = getattr(settings, 'QUOTAS', {})

def _user_get_quota(user, base):
    """Return user's quota for `base'.

    Returns True if unlimited, integer if limited, None if no quota was set."""
    def __has_quota_of(limit):
        return user.has_perm( 'quotas.quota_%s_%s'%(base, limit) )
    if __has_quota_of('unlimited'): return INFINITY
    try:
        for v in sorted( QUOTAS[base], reverse=True ):
            if __has_quota_of(v):
                return v
    except KeyError: pass               # no base quota
    return None
# User.add_to_class('get_quota', _user_get_quota)

class UserQuotas(object):
    def __init__(self, user):
        self.__user = user
    def __getattr__(self, quota_name):
        if quota_name in QUOTAS:
            return _user_get_quota(self.__user, quota_name)
        raise AttributeError

def _user_get_quotas(user):
    return UserQuotas(user)

User.add_to_class('quotas', property(_user_get_quotas))

