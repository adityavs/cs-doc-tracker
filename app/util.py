from flask import url_for

def get_url(url_template, params, key = None, value = None):
    if not params:
        params = {}
    if key:
        params[key] = value
    return url_for(url_template, **params)
