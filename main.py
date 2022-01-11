import pyperclip
import sys

from formatter import format

DEFAULT_LANG = 'java'

def copy_paste(code='', language=DEFAULT_LANG, output=False, clipboard=False) -> str:
    """
    Returns code in HTML format. Copies to clipboard if CLIPBOARD is true
    :param str code: code to format
    :param str language: parameter to specify language - default is 'java'
    :param bool output: records HTML in ../output.txt if TRUE
    :param bool clipboard: copies to clipboard if TRUE
    """
    formatted_code = format(code, language)
    print(f'Converting {language} to HTML \n\n{code}\n')
    if output:
        with open('output.txt', 'w') as f:
            f.write(formatted_code)
            print(f'Outputted to {f.name}')
    if clipboard:
        pyperclip.copy(formatted_code)
        print('Copied to clipboard!')
    return formatted_code

if __name__ == '__main__':
    """
    The first argument of the CLI arguments must be the language (default is Java). 
    Add -o after the language to output to output.txt in current directory
    """
    language = DEFAULT_LANG
    output = False
    for arg in sys.argv[1:]:
        # for all extra arguments, set output flag=TRUE OR language=last_arg
        if arg == '-o':
            output = True
        else:
            language = arg
    code = pyperclip.paste()
    copy_paste(code, language, output, True)
