NE = IS_NOT_EMPTY()
ADMIN, USER = "admin", "user"

db.define_table(
    "organization",
    Field('name', unique=True, required=True),
    Field('accounts', 'integer', default=10))

db.define_table(
    'membership',
    Field('organization', 'reference organization', requires=NE),
    Field('auth_user', 'reference auth_user'),
    Field('role', requires=IS_IN_SET((ADMIN, USER))),
    auth.signature)

db.define_table(
    "projects",
    Field('name', 'string', required=True),
    Field('organization', 'reference organization', required=True),
    Field('city', 'string'),
    Field('proj_state', 'string'),
    Field('proj_origin', 'double'),
    Field('point_count', 'integer')
)