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


def book_serializer(obj, no_author):
    if no_author:
        return {
            'id': obj.id,
            'created': dump_datetime(obj.created),
            'isbn': obj.isbn,
            'title': obj.title,
            'number_of_pages': obj.number_of_pages,
            'review': obj.review,
            'owner': obj.owner.name,
        }
    return {
        'id': obj.id,
        'created': dump_datetime(obj.created),
        'isbn': obj.isbn,
        'title': obj.title,
        'number_of_pages': obj.number_of_pages,
        'review': obj.review,
        'author': author_serializer(obj.author),
        'owner': owner_serializer(obj.owner),
    }


def user_serializer(obj):
    return {
        'id': obj.id,
        'name': obj.name,
        'email': obj.email,
        'books': [book_serializer(book, False) for book in obj.books],
        'authors': [author_serializer(author) for author in obj.authors],
    }
