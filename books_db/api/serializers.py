def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime('%Y-%m-%d %H:%M:%S')


def author_serializer(obj):
    return {
        'id': obj.id,
        'created': dump_datetime(obj.created),
        'isbn': obj.isbn,
        'fio': obj.fio,
    }


def authors_serializer(query):
    return [author_serializer(obj) for obj in query]


def books_serializer(query):
    serialized_query = []
    for obj in query:
        serialized_query.append({
            'id': obj.id,
            'created': dump_datetime(obj.created),
            'isbn': obj.isbn,
            'title': obj.title,
            'number_of_pages': obj.number_of_pages,
            'review': obj.review,
            'author': author_serializer(obj.author),
        })
    return serialized_query


def books_without_author_serializer(query):
    serialized_query = []
    for obj in query:
        serialized_query.append({
            'id': obj.id,
            'created': dump_datetime(obj.created),
            'isbn': obj.isbn,
            'title': obj.title,
            'number_of_pages': obj.number_of_pages,
            'review': obj.review,
        })
    return serialized_query
