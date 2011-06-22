# modified from http://djangosnippets.org/snippets/67/

# use in templates:
#
#   {% load value_from_settings %}
#
#   ...{% value_from_settings FOOBAR %}...
#


from django import template
import settings
register = template.Library()

@register.tag
def value_from_settings ( parser, token ): 
    try:
        tag_name, option = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents[0]
    return SettingNode( option )

class SettingNode ( template.Node ): 
    def __init__ ( self, option ): 
        self.option = option

    def render ( self, context ): 
        return str( getattr(settings, self.option) )
