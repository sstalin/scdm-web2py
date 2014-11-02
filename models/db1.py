__author__ = 'sstalin'

NE = IS_NOT_EMPTY()
ADMIN, USER = "admin", "user"

# initially each organization will have up to 10 accounts
db.define_table(
    "organization",
    Field('name', unique=True, required=True),
    format='%(name)s'
)

db.define_table(
    'membership',
    Field('organization', 'reference organization'),
    Field('auth_user', 'reference auth_user'),
    Field('role', requires=IS_IN_SET((ADMIN, USER))),
    auth.signature)

db.membership.auth_user.requires = IS_NOT_IN_DB(db(db.membership.organization == request.vars.organization),
                                                'membership.auth_user')

db.define_table(
    'layer',
    Field('name', requires=NE),
    Field('organization', 'reference organization', readable=False, writable=False),
    Field('filename', 'upload', label='Content'),
    Field('updated_on', 'datetime', update=request.now),
    Field('updated_by', db.auth_user, update=auth.user_id),
    auth.signature)


def get_user_info(user=auth.user_id):
    if user:
        row = db(db.membership.auth_user == user).select().first()
        organization_id = None
        organization_name = None
        if row:
            organization_id = row.organization
            organization_name = db(db.organization.id == organization_id).select().first().name
        first_name = db(db.auth_user.id == user).select().first().first_name
        last_name = db(db.auth_user.id == user).select().first().last_name
        return dict(first_name=first_name, last_name=last_name, organization_name=organization_name,
                    organization_id=organization_id)
    else:
        return {}


if db(db.auth_user).isempty():
    from gluon.contrib.populate import populate

    mdp_id = db.auth_user.insert(first_name="Good", last_name='Teacher',
                                 email='good.teacher@example.com',
                                 password=CRYPT()('test')[0])
    ss_id = db.auth_user.insert(first_name="Svetlin", last_name='Stalinov',
                                email='ss@example.com',
                                password=CRYPT()('test')[0])

    populate(db.organization, 4)
    populate(db.auth_user, 8)
    populate(db.membership, 10)

    db(db.membership.auth_user < 3).update(role=ADMIN)
    db(db.auth_user.id > 2).update(is_administrator=False)