__author__ = 'sstalin'

NE = IS_NOT_EMPTY()
MANAGER, USER = "data_manager", "user"
SHOW_FOOTER = False

# initially each organization will have up to 10 accounts
db.define_table(
    "organization",
    Field('name', 'string', requires=NE),
    Field('members', 'integer', readable=False, writable=False, default=1)
)

db.organization.name.requires = IS_NOT_IN_DB(db, 'organization.name')

db.define_table(
    'membership',
    Field('auth_user', 'reference auth_user', readable=False, writable=False),
    Field('organization', 'reference organization'),
    Field('role', requires=IS_IN_SET((MANAGER, USER))),
    auth.signature)

db.membership.auth_user.requires = IS_NOT_IN_DB(db(db.membership.organization == request.vars.organization),
                                                'membership.auth_user')
# db.membership.organization.requires = IS_IN_DB(db, db.organization.id, '%(name)s')
# db.membership.auth_user.requires = IS_IN_DB(db, db.auth_user.id, '%(email)s')


db.define_table(
    'layers',
    Field('name', requires=NE),
    Field('organization', 'reference organization', readable=False, writable=False),
    Field('description', 'text', requires=IS_LENGTH(100)),
    Field('filename', 'upload', autodelete=True),
    auth.signature)


def get_user_info(user=auth.user_id):
    """
    Retrieves default user information, or information for given user_id
    :param user: user_id
    :return: User info object as dictionary
    """
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


def set_membership(user=auth.user_id, org_id=None, role='user'):
    return db.membership.insert(auth_user=user, organization=org_id, role=role)


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

    db(db.membership.auth_user < 3).update(role=MANAGER)
    db(db.auth_user.id > 2).update(is_administrator=False)