from flask_restx import fields

class NullableUrl(fields.Url):
    def schema(self):
        schema = super(NullableUrl, self).schema()
        schema.update(type=['url', 'null'])
        return schema
    