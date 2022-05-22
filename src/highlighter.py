# Ink Editor - highlighter.py
# github.com/leftbones/ink

import os, curses

from logger import log

import pygments
import pygments.lexers
from pygments.styles import get_style_by_name
from pygments.formatter import Formatter

class InkFormatter(Formatter):
    def __init__(self, **options):
        Formatter.__init__(self, **options)

        self.styles = {}

        for token, style in self.style:
            start = end = ''

            if style['color']:
                start += '<ink_color_on %s>' % style['color']
                end = '<ink_color_off>' + end
            self.styles[token] = (start, end)

    def format(self, tokensource, outfile):
        lastval = ''
        lasttype = None

        for ttype, value in tokensource:
            while ttype not in self.styles:
                ttype = ttype.parent
            if ttype == lasttype:
                lastval += value
            else:
                if lastval:
                    stylebegin, styleend = self.styles[lasttype]
                    outfile.write(stylebegin + lastval + styleend)
                lastval = value
                lasttype = ttype

        if lastval:
            stylebegin, styleend = self.styles[lasttype]
            outfile.write(stylebegin + lastval + styleend)


class Highlighter:
    def __init__(self, terminal):
        self.terminal = terminal
        self.formatter = None
        self.style = None

    def match_lexer(self, path):
        self.style = get_style_by_name(self.terminal.config.colorscheme)
        self.formatter = InkFormatter(style=self.style)

        self.terminal.colorizer.default_fg = list(self.style.styles.values())[0][1:] # This is gross.
        self.terminal.colorizer.default_bg = self.style.background_color[1:]

        filename = os.path.basename(path).split()[-1]

        try: self.lexer = pygments.lexers.get_lexer_for_filename(filename)
        except: self.terminal.cursor.window.hlsyntax = False

        self.terminal.cursor.window.language = self.detect_language(path)

    def hl(self, code):
        return pygments.highlight(code, self.lexer, self.formatter)

    def detect_language(self, path):
        extension = os.path.basename(path).split('.')[-1]
        match extension:
            case 'ada':     return 'ada'
            case 'bf':      return 'brainfuck'
            case 'c':       return 'c'
            case 'cmake':   return 'cmake'
            case 'cpp':     return 'c++'
            case 'cs':      return 'c sharp'
            case 'css':     return 'css'
            case 'd':       return 'd'
            case 'frt':     return 'forth'
            case 'go':      return 'go'
            case 'h':       return 'c'
            case 'ha':      return 'hare'
            case 'hpp':     return 'cpp'
            case 'html':    return 'html'
            case 'inkrc':   return 'inkrc'
            case 'jl':      return 'julia'
            case 'js':      return 'javascript'
            case 'json':    return 'json'
            case 'lua':     return 'lua'
            case 'make':    return 'makefile'
            case 'md':      return 'markdown'
            case 'nim':     return 'nim'
            case 'php':     return 'php'
            case 'py':      return 'python'
            case 'rb':      return 'ruby'
            case 'rs':      return 'rust'
            case 'rtf':     return 'rich text'
            case 'swift':   return 'swift'
            case 'ts':      return 'typescript'
            case 'txt':     return 'text'
            case 'yaml':    return 'yaml'
            case 'zig':     return 'zig'
            case _:         return extension
