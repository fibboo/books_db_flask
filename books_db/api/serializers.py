def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    print(value)
    return value.strftime('%Y-%m-%d %H:%M:%S')


def author_serializer(obj):
    return {
        'id': obj.id,
        'created': dump_datetime(obj.created),
        'isbn': obj.isbn,
        'fio': obj.fio,
    }


def owner_serializer(obj):
    return {
        'id': obj.id,
        'name': obj.name,
        'email': obj.email,
    }


def authors_serializer(query):
    return [author_serializer(obj) for obj in query]


def book_to_dict(obj, no_author):
    if no_author:
        return {
            'id': obj.id,
            'created': dump_datetime(obj.created),
            # 'published': dump_datetime(obj.published),
            'isbn': obj.isbn,
            'title': obj.title,
            'number_of_pages': obj.number_of_pages,
            'review': obj.review,
            'owner': obj.owner.name,
        }
    return {
        'id': obj.id,
        'created': dump_datetime(obj.created),
        # 'published': dump_datetime(obj.published),
        'isbn': obj.isbn,
        'title': obj.title,
        'number_of_pages': obj.number_of_pages,
        'review': obj.review,
        'author': author_serializer(obj.author),
        'owner': owner_serializer(obj.owner),
    }


def book_serializer(obj, no_author):
    return book_to_dict(obj, no_author)
