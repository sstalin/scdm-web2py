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
        # # if newly registered user is not in auth_membership add him as an administrator
        if not db(db.auth_membership.user_id == auth.user_id).count() > 0:
            auth.add_membership(auth.id_group(ADMIN), auth.user_id)
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


@auth.requires_permission('add', 'users')
def admin():
    return dict()


def people():
    """
    People in organization
    :return: list of users
    """
    # users = get_users()
    return dict()


# @service.json
# def users():
# """
# People in organization
#     :return: list of users
#     """
#     users = get_users()
#     return users


@request.restful()
def users():
    response.view = 'generic.json'

    def GET(*args, **vars):
        users = get_users()
        return dict(users=users)

    def POST(*args, **vars):
        users = vars['users']
        count = 0
        for user in users:
            if user:
                count += db(db.auth_user.id == user.get('auth_user').get('id')).delete()
        flash = str(count) + " users deleted!"
        users = get_users()
        return dict(users=users, flash=flash)

    return locals()


def add_user():
    """
    Adds new user with selected rights to database with default password : password. Email is sent optionally.
    :return:
    """
    form = FORM(
        H4('First Name:', _for='first_name'),
        INPUT(_name='first_name', _type='text', requires=IS_NOT_EMPTY()),
        H4('Last Name:', _for='last_name'),
        INPUT(_name='last_name', _type='text', requires=IS_NOT_EMPTY()),
        H4('Email:', _for='email'),
        INPUT(_name='email', _type='email', requires=IS_NOT_EMPTY()),
        DIV(INPUT(_name='isAdmin', _type='checkbox'),
            LABEL('Administrator', _for='isAdmin')),
        BR(),
        DIV(INPUT(_name='isDataManager', _type='checkbox'),
            LABEL('Data Manager', _for='isDataManager')),
        BR(),
        DIV(INPUT(_name='sendEmail', _type='checkbox'),
            LABEL('Send Email', _for='sendEmail')),
        INPUT(_value='+ Add User', _type='submit', _class='right'),
        INPUT(_value='Reset', _type='reset', _class='right btn')
    )
    form.process()
    if form.accepted:
        fn = form.vars.first_name
        ln = form.vars.last_name
        email = form.vars.email
        role = USER
        if form.vars.isDataManager:
            role = MANAGER
        if form.vars.isAdmin:
            role = ADMIN
        try:
            if is_email_exist(email):
                response.flash = "Email exist in database"
                raise IOError
            usr_id = create_new_user(fn, ln, email, role)
            if usr_id > 0:
                if form.vars.sendEmail:
                    # TODO
                    response.flash = "Invitation has been sent"
                else:
                    response.flash = 'User added successfully'
        except IOError:
                response.flash = "Email exist in database"
        except Exception:
            response.flash = 'Error while processing'
    elif form.errors:
        response.flash = 'form has errors'
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
