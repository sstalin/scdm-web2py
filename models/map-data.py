db.define_table(
    'layer',
    Field('name', requires=NE),
    Field('organization', 'reference organization', readable=False, writable=False),
    Field('filename', 'upload', label='Content'),
    Field('updated_on', 'datetime', update=request.now),
    Field('updated_by', db.auth_user, update=auth.user_id),
auth.signature)
