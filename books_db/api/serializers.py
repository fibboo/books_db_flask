def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    print(value)
    return value.strftime('%Y-%m-%d %H:%M:%S')


def owner_serializer(obj):
    return {
        'id': obj.id,
        'username': obj.username,
        'email': obj.email,
    }


def author_serializer(obj, owner=False):
    serialized_data = {
        'id': obj.id,
        'created': dump_datetime(obj.created),
        'isbn': obj.isbn,
        'fio': obj.fio,
    }
    if owner:
        serialized_data.update({'owner': owner_serializer(obj.owner)})
    return serialized_data


def book_serializer(obj, with_author=False, owner=False):
    serialized_data = {
        'id': obj.id,
        'created': dump_datetime(obj.created),
        'isbn': obj.isbn,
        'title': obj.title,
        'number_of_pages': obj.number_of_pages,
        'review': obj.review,
    }
    if with_author:
        serialized_data.update({'author': author_serializer(obj.author)})
    if owner:
        serialized_data.update({'owner': owner_serializer(obj.owner)})
    return serialized_data


def user_serializer(obj, with_authors=False, with_books=False):
    serialized_data = {
        'id': obj.id,
        'username': obj.username,
        'email': obj.email,
    }
    if with_authors:
        serialized_data.update(
            {'authors': [author_serializer(author) for author in obj.authors]}
        )
    if with_books:
        serialized_data.update(
            {'books': [book_serializer(book, False) for book in obj.books]}
        )
    return serialized_data
