__author__ = 'sstalin'

NE = IS_NOT_EMPTY()
ADMIN, USER = "admin", "user"

# initially each organization will have up to 10 accounts
db.define_table(
    "organization",
    Field('name', unique=True, required=True),
    Field('accounts', 'integer', default=10),
    format='%(name)s'
)

db.define_table(
    'membership',
    Field('organization', 'reference organization', requires=NE),
    Field('auth_user', 'reference auth_user'),
    Field('role', requires=IS_IN_SET((ADMIN, USER))),
    auth.signature)


# db.define_table(
# "projects",
# Field('name', 'string', required=True),
# Field('organization', 'reference organization', required=True),
# Field('city', 'string'),
# Field('proj_state', 'string'),
# Field('proj_origin', 'double'),
# Field('point_count', 'integer')
# )

if db(db.auth_user).isempty():
    import datetime
    from gluon.contrib.populate import populate

    mdp_id = db.auth_user.insert(first_name="Good", last_name='Teacher',
                                 email='good.teacher@example.com',
                                 password=CRYPT()('test')[0])
    ss_id = db.auth_user.insert(first_name="Svetlin", last_name='Stalinov',
                                email='ss@example.com',
                                password=CRYPT()('test')[0])
    populate(db.auth_user, 10)
    db(db.auth_user.id > 1).update(is_administrator=False)