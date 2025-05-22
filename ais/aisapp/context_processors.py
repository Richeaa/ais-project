def inject_username(request):
    return {
        'username': request.session.get('username')
    }