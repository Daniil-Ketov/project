from django.template.loader_tags import register


@register.inclusion_tag("blocks/comment.html")
def place_comment(comment):
    return {'comment': comment}

@register.simple_tag
def get_companion(user, chat):
    for u in chat.members.all():
        if u != user:
            return u
    return None

