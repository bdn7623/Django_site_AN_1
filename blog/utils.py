from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate_objects(request, objects_list, num_per_page=2):
    """
    Paginate a list of objects.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param objects_list: The list of objects to paginate.
    :type objects_list: list
    :param num_per_page: The number of objects per page (default is 2).
    :type num_per_page: int
    :return: Paginated objects.
    :rtype: django.core.paginator.Page
    """
    paginator = Paginator(objects_list, num_per_page)
    page = request.GET.get('page')

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objects = paginator.page(paginator.num_pages)

    return objects
