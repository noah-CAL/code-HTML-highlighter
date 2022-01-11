"""Defines format() function to format code into HTML tags to be read by Anki in combination w/ CSS selectors"""
from pygments import highlight
from pygments.formatters import HtmlFormatter

# import lexers for each language
from pygments.lexers import PythonLexer
from pygments.lexers.javascript import JavascriptLexer
from pygments.lexers.html import HtmlLexer
from pygments.lexers.shell import BashLexer
from pygments.lexers.lisp import SchemeLexer
from pygments.lexers.jvm import JavaLexer

def format(code: str, lang: str ) -> str: 
    """
    Takes input code and returns a string of HTML with approriate <div> / <span> classes
    :param str code: code to format
    :param str lang: OPTIONAL parameter to specify language - default is 'python', options are currently: 'python' 'javascript' 'bash' 'html' 'scheme' 'java'
    """
    lexers = {
        'python': PythonLexer,
        'javascript': JavascriptLexer,
        'bash': BashLexer,
        'html': HtmlLexer,
        'scheme': SchemeLexer,
        'java': JavaLexer,
        # etc...
    }
    if lang not in lexers:
        raise KeyError(f'{lang} is not an available lexer. Acceptable keys are {lexers.keys()}')
    lexer = lexers[lang]
    formatted = highlight(code, lexer(), HtmlFormatter())

    # add language class to container div
    div = f'<div class="highlight {lang}">'
    return formatted.replace('<div class="highlight">', div)
