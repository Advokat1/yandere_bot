from orator import Model, scope


class Img(Model):
    __table__ = 'images'
    __incrementing__ = False
    __timestamps__ = True
    __fillable__ = ['id', 'tags', 'author', 'source', 'file_url', 'score', 'rating', 'is_rating_locked', 'has_children']
    __casts__ = {
        'id': 'int',
        'tags': 'list',
        'score': 'int',
        'is_rating_locked': 'bool',
        'has_children': 'bool'
    }

    @scope
    def has_no_children(self, query):
        return query.where('has_children', '=', False)

    @scope
    def normal(self, query):
        return query\
            .where('is_rating_locked', '=', False)\
            .where('has_children', '=', False)\
            .where('rating', '<>', 'e')

