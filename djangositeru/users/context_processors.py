from blog.utils import menu

"""контекстные процессоры
    нужно подключить в настройках
"""

def get_blog_context(request):
    return {'mainmenu': menu}