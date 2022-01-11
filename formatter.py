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

import re

def replace_cloze(matchobj) -> str:
    """Higher-order to be used as REPL argument in re.sub() to replace clozes after formatting has occurred"""
    print(matchobj.group(0))
    print(matchobj.group(1))
    print('\n')

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

    # replace clozes in match for anki formatting
    pattern = (r'<span class="p">{{</span><span class="n">c\d</span><span class="p">::</span>' # matches '{{c1::'
            + r'([\S\s]*?)' # capture group inside cloze -- text should be preserved in substitution -- matches any character incl. newline
            + r''           # TODO include support for optional cloze hints
            + r'<span class="p">}}</span>') # matches closing brackets '}}'
    formatted = re.sub(pattern, replace_cloze, formatted)

    # add language class to container div
    div = f'<div class="highlight {lang}">'
    return formatted.replace('<div class="highlight">', div)
