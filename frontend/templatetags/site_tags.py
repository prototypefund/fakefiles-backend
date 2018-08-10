from django import template


register = template.Library()


@register.inclusion_tag('includes/_breadcrumbs.html', takes_context=True)
def render_breadcrumbs(context):
    if 'flatpage' in context:
        flatpage = context['flatpage']
        return {
            'breadcrumbs': ({
                'name': flatpage.title,
                'url': flatpage.url
            },)
        }
    if 'item' in context:
        item = context['item']
        return {
            'breadcrumbs': ({
                'name': item.name,
                'url': item.get_absolute_url()
            },)
        }
    else:
        # FIXME
        return
