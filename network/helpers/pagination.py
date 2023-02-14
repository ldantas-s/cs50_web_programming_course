from django.core.paginator import Paginator

obj_per_page = 4


def pagination(objs, page_number=1):
    paginator = Paginator(objs, obj_per_page)
    page_obj = paginator.get_page(page_number)

    return page_obj
