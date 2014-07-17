from datetime import datetime

import six

from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


tz_now = timezone.now

def friendly_datetime(date_time):
    """
    Given a datetime object or an int() Unix timestamp, return a friendly
    string like 'an hour ago', 'yesterday', '3 months ago', 'just now', etc.
    """
    now = tz_now()
    if type(date_time) is datetime:
        diff = now - date_time
    elif type(date_time) is int:
        diff = now - datetime.fromtimestamp(date_time)
    else:
        return date_time

    seconds_diff = diff.seconds
    days_diff = diff.days

    if days_diff < 0:
        return ''

    if days_diff == 0:
        if seconds_diff < 10:
            return six.text_type(_('just now'))
        if seconds_diff < 60:
            return _('%s seconds ago') % str(seconds_diff)
        if seconds_diff < 120:
            return six.text_type('a minute ago')
        if seconds_diff < 3600:
            return _('%s minutes ago') % str(seconds_diff // 60)
        if seconds_diff < 7200:
            return six.text_type(_('an hour ago'))
        if seconds_diff < 86400:
            return _('%s hours ago') % str(seconds_diff // 3600)
    if days_diff == 1:
        return six.text_type(_('yesterday'))
    if days_diff < 7:
        return _('%s days ago') % str(days_diff)
    if days_diff < 14:
        return six.text_type(_('a week ago'))
    if days_diff < 31:
        return _('%s weeks ago') % str(days_diff // 7)
    if days_diff < 365:
        return _('%s months ago') % str(days_diff // 30)
    return _('%s years ago') % str(days_diff // 365)
