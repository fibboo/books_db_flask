from flask import make_response, jsonify, abort


def check_object_permission(current_user, obj):
    if current_user != obj.owner:
        abort(make_response(jsonify({'detail': 'You do not have sufficient '
                                               'rights to perform this '
                                               'action.'}), 403))


def check_self_permission(current_user, obj):
    if current_user != obj:
        abort(make_response(jsonify({'detail': 'You do not have sufficient '
                                               'rights to perform this '
                                               'action.'}), 403))
