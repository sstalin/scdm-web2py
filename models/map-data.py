db.define_table(
    'organizationMarkers',
    Field('pid', required=True),
    Field('ptName', 'string'),
    Field('Lat', 'double'),
    Field('Long', 'double'),
    Field('description', 'string'),
    Field('project', 'reference project'),
    Field('organization', 'reference organization'),
)
