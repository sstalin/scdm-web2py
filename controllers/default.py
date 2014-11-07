# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ########################################################################
# # This is a sample controller
# # - index is the default action of any application
# # - user is required for authentication and authorization
# # - download is for downloading files uploaded in the db (does streaming)
# # - api is an example of Hypermedia API support and access control
# ########################################################################


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    if auth.is_logged_in():
        session.user_info = get_user_info()
        response.user_info = session.user_info
    if request.user_agent().is_mobile:
        return response.render('../views/default/index-m.html')
    else:
        return response.render('../views/default/index.html')


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    form = auth()
    return dict(form=form)


@auth.requires_login()
def set_organization():
    """
    Creates form for registering organization and
    creates membership.
    :return: form
    """
    form = SQLFORM(db.organization, labels={'name': ''})
    if form.process().accepted:
        org_id = form.vars.id
        session.org_id = org_id
        session.mem_id = set_membership(auth.user_id, org_id, MANAGER)
        session.flash = "Organization: " + form.vars.name + " was created"
        redirect(URL('index'))
    elif form.errors:
        if form.errors.name == 'Value already in database or empty':
            response.flash = form.vars.name + " name exist in database!"
            form.errors.name = None

    return dict(form=form)


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login()
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection

    rules = {
        '<tablename>': {'GET': {}, 'POST': {}, 'PUT': {}, 'DELETE': {}},
    }
    return Collection(db).process(request, response, rules)
