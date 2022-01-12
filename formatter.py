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

def remove_cloze(string) -> str:
    """Remove Anki-style cloze tags from HTML strings"""

    # Match group index:
    # 1 -- pre_punctuation before {{
    # 2 -- cloze_number n in {{c(n)::
    # 3 -- capture group inside close {{cn::(text)}}
    # 4 -- capture group inside hint ::(hint)}}
    # 5 -- post_punctuation_before ()}}  i.e. should be inside (text) or (hint)
    # 6 -- post_punctuation_after }}()   i.e. should remain outside }}
    pattern = (r'<span class="p">(.*){{</span>'                             # matches '{{' and pre-punc e.g. 'JavaObj.{{c1'
            + r'<span class="n">c(\d+?)</span><span class="p">::</span>'    # matches 'cn::' 
            + r'([\S\s]*?)'                                                 # matches any character incl. newline inside cloze
            + r'(?:<span class="p">::</span>([\S\s]*?))?'                   # optional cloze hints -- matches hint in match_group 4
            + r'<span class="p">(.*)}}(.*?)</span>')                        # matches '}}' and post-punc_before/after

    def repl(matchobj):
        pre_punc            = matchobj.group(1)
        cloze_number        = matchobj.group(2)
        cloze_text          = matchobj.group(3)
        optional_hint       = matchobj.group(4)
        post_punc_before    = matchobj.group(5)
        post_punc_after     = matchobj.group(6)

        # Wrap punctuation in <span> tags
        span_wrapper = lambda text, tag='p': f'<span class="{tag}">{text}</span>' if text else ''
        pre_punc          = span_wrapper(pre_punc)
        post_punc_before  = span_wrapper(post_punc_before)
        post_punc_after   = span_wrapper(post_punc_after)

        # format hint to anki format
        hint = '::' + optional_hint if optional_hint else ''

        return pre_punc + '{{c' + cloze_number + '::' + cloze_text + hint + post_punc_before + '}}' + post_punc_after

    return re.sub(pattern, repl, string)

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
    formatted = formatted.replace('<div class="highlight">', div)

    return remove_cloze(formatted)

# TEST CODE for cloze_remover with punctation before/after cloze tags
# /* HelloWorld.java */ 

# public class HelloWorld { 
#     public static void main(String[] args) { 
#         System.out.{{c1::println("Hello World!")}}; 
#     } 
# }