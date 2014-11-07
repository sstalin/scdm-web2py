__author__ = 'sstalin'


@auth.requires_login()
def lay_manage():
    """
    Adds new layer for the current organization.
    :return:
    """
    record = db.layers(request.args(0))
    if record:
        message = 'layer edited successfully!'
        btn_value = 'edit'
    else:
        message = 'layer added successfully!'
        btn_value = 'add'

    form = SQLFORM(db.layers, record, deletable=True,
                   upload=URL('download'))

    if form.process().accepted:
        lay_id = form.vars.id
        db(db.layers.id == lay_id).update(organization=session.user_info['organization_id'])
        session.flash = message
        if record:
            redirect(URL('lay_manage'))
    return locals()


def download():
    return response.download(request, db)


@auth.requires_login()
def lay_all():
    """
    All layers that belong to current organization.

    :return: list of layers
    """
    layers = db(db.layers.organization == session.user_info['organization_id']).select('name', 'id')
    return locals()


