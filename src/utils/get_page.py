def _get_previous_page_url(request, default_url):
    referer = request.META.get('HTTP_REFERER')
    return referer or default_url
