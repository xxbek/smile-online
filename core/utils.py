import os
from io import BytesIO
from django.template.loader import get_template

from xhtml2pdf import pisa

from smile_online import settings


def fetch_resources(uri, rel):
    """
    Retrieves embeddable resource from given ``uri``.

    For now only local resources (images, fonts) are supported.

    :param str uri: path or url to image or font resource
    :returns: path to local resource file.
    :rtype: str
    """
    if settings.STATIC_URL and uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
    elif settings.MEDIA_URL and uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    else:
        path = os.path.join(settings.STATIC_ROOT, uri)

    return path.replace("\\", "/")


def render_to_pdf(template_src, context_dict, filename, ):
    template = get_template(template_src)
    context_dict['STATIC_ROOT'] = settings.STATIC_ROOT
    context_dict['pdf'] = '1'
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(html.encode('utf-8')), result, encoding='UTF-8', link_callback=fetch_resources, )

    if not pdf.err:
        return result.getvalue()

    raise Exception('PDF generation error')
