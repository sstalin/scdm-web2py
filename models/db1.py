__author__ = 'sstalin'

NE = IS_NOT_EMPTY()
ADMIN, MANAGER, USER = "administrator", "data_manager", "user"
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


## HELPERS

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


def get_users(organization=None):
    """
    Retrieves all users for given organization.
    :param org_id:
    :return: list of users
    """
    org_id = organization or db(db.membership.auth_user == auth.user_id).select('organization').first().organization
    users_in_organization = db((db.membership.organization == db.organization.id)
                               & (db.auth_user.id == db.membership.auth_user)
                               & (db.organization.id == org_id)
                               & (db.auth_user.id != auth.user_id)).select()
    return users_in_organization


def get_role(user_id = auth.user_id):
    """
    Retrieves role for given user id
    :param user_id:
    :return: role associated with user
    """
    group_id = db(db.auth_membership.user_id == user_id).select('group_id').first().group_id
    return db(db.auth_group.id == group_id).select('role').first().role


def set_membership(user=auth.user_id, org_id=None):
    """
    Set membership with given parameters.
    :param user:
    :param org_id:
    :param role:
    :return:
    """
    return db.membership.insert(auth_user=user, organization=org_id)


def create_new_user(fn, ln, email, role):
    usr_id =db.auth_user.insert(first_name=fn, last_name=ln,
                                 email=email,
                                 password=CRYPT()('password')[0])
    if usr_id > 0:
        org_id = get_user_info()['organization_id']
        mem_id = set_membership(usr_id, org_id)
        group_id = auth.id_group(role)
        auth_mem_id= auth.add_membership(group_id, usr_id)
        return usr_id
    return None


def is_email_exist(email):
    return db(db.auth_user.email == email).count() > 0



##################### populate database #####################

if db(db.auth_group).isempty():
    ### create groups
    admin_group_id = auth.add_group(ADMIN, 'Administrator role')
    manager_group_id = auth.add_group(MANAGER, 'Manager role')
    user_group_id = auth.add_group(USER, 'Regular user role')

if db(db.auth_permission).isempty():
    ## add permissions for administrators
    auth.add_permission(admin_group_id, 'add', 'users')
    auth.add_permission(admin_group_id, 'remove', 'users')
    auth.add_permission(manager_group_id, 'manage', 'layers')
    ## add permissions for data managers
    auth.add_permission(manager_group_id, 'manage', 'layers')
    ## add permissions for regular user
    auth.add_permission(user_group_id, 'read', db.layers, 0)


if db(db.auth_user).isempty():
    from gluon.contrib.populate import populate

    mdp_id = db.auth_user.insert(first_name="Good", last_name='Teacher',
                                 email='good.teacher@example.com',
                                 password=CRYPT()('test')[0])
    ss_id = db.auth_user.insert(first_name="Svetlin", last_name='Stalinov',
                                email='ss@example.com',
                                password=CRYPT()('test')[0])

    populate(db.auth_user, 8)
    db(db.auth_user.id > 2).update(is_administrator=False)

    users = db(db.auth_user).select()
    org_id = db.organization.insert(name="ss_Solution")
    for user in users[0:5]:
        user_id = user.id
        db.membership.insert(auth_user=user_id, organization=org_id)
        auth.add_membership(user_group_id, user_id)

    org_id = db.organization.insert(name="X_Solution")
    for user in users[5:10]:
        user_id = user.id
        db.membership.insert(auth_user=user_id, organization=org_id)
        auth.add_membership(user_group_id, user_id)

    db(db.organization.name == "ss_Solution").update(members=5)
    db(db.organization.name == "X_Solution").update(members=5)

    db(db.auth_membership.id < 3).update(group_id=admin_group_id)
    db(db.auth_membership.id > 8).update(group_id=admin_group_id)


    # populate(db.organization, 4)
    # populate(db.auth_user, 8)
    # populate(db.membership, 10)
    #
    # db(db.membership.auth_user < 3).update(role=MANAGER)
    # db(db.auth_user.id > 2).update(is_administrator=False)