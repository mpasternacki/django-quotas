class Unlimited(object):
    is_unlimited = True

    def __cmp__(self, other):
        return 1

    def __gt__(self, other):
        return True

    def __ge__(self, other):
        return True

    def __eq__(self, other):
        return False

    def __le__(self, other):
        return False

    def __lt__(self, other):
        return False

    def __unicode__(self):
        return u'unlimited'
    

UNLIMITED = Unlimited()
