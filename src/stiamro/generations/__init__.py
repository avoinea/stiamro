from zope.app.generations.generations import SchemaManager

StiamSchemaManager = SchemaManager(
    minimum_generation=0,
    generation=5,
    package_name='stiamro.generations'
)
