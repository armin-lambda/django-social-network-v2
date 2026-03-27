def send_sms(phone_number, message):
    print(f"\n\n{phone_number} - {message}\n\n")


INVALID_NAMES = [
    # Authentication & User
    'username', 'user', 'users', 'email', 'first_name', 'last_name',
    'password', 'confirm_password', 'auth', 'account', 'profile',
    'signup', 'signin', 'signout', 'register', 'login', 'logout',
    'verify', 'verification', 'token', 'session',

    # CRUD / Actions
    'create', 'update', 'upgrade', 'delete', 'remove', 'edit', 'change',
    'patch', 'put', 'post', 'get', 'list', 'detail', 'retrieve',

    # Common API endpoints
    'posts', 'comments', 'likes', 'follow', 'unfollow', 'explore',
    'feed', 'search', 'settings', 'config', 'admin', 'dashboard',

    # Generic reserved words
    'field', 'section', 'setting', 'option', 'value', 'data', 'info',
    'item', 'object', 'instance', 'model', 'serializer', 'view',

    # System / backend related
    'root', 'base', 'main', 'core', 'index', 'static', 'media',
    'public', 'private', 'internal', 'external',

    # Security / sensitive
    'api', 'api_key', 'secret', 'key', 'keys', 'hash', 'encrypt',
    'decrypt', 'secure', 'security',

    # HTTP / Web
    'request', 'response', 'url', 'uri', 'route', 'endpoint', 'path',

    # Misc
    'test', 'testing', 'debug', 'sample', 'example', 'demo',
]
