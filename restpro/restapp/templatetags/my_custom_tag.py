# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

class AssignNode(template.Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def render(self, context):
        context[self.name] = self.value.resolve(context, True)
        return ''

def do_assign(parser, token):
    """
    Assign an expression to a variable in the current context.
    
    Syntax::
        {% set [name] [value] %}
    Example::
        {% set list entry.get_related %}
        
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    value = parser.compile_filter(bits[2])
    return AssignNode(bits[1], value)

# 自定义tag,可用来在模板中设置变量
register.tag('set', do_assign)

# 自定义filter
@register.filter
@stringfilter
def lower(value):
    return value.lower()
