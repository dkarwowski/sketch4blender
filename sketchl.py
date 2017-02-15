import os
import ply.lex as lex
from ply.lex import TOKEN

class Lexer:
    keyword_tokens = [ 'LANGUAGE'  , 'PSTRICKS' , 'TIKZ'    , 'LaTeX'      , 'ConTeXt'     ,
                       'CURVE'     , 'CAMERA'   , 'DEF'     , 'DOTS'       , 'FRAME'       ,
                       'GLOBAL'    , 'LINE'     , 'POLYGON' , 'PUT'        , 'REPEAT'      ,
                       'SET'       , 'SWEEP'    , 'THEN'    , 'PICTUREBOX' , 'ASIN'        ,
                       'ACOS'      , 'ATAN2'    , 'COS'     , 'INVERSE'    , 'PERSPECTIVE' ,
                       'PROJECT'   , 'ROTATE'   , 'SCALE'   , 'SIN'        , 'SQRT'        ,
                       'TRANSLATE' , 'UNIT'     , 'VIEW'    ]

    reserved = { keyword.lower() : keyword for keyword in keyword_tokens }

    # TODO(david): remove reserved words from having to be input manually
    tokens = [ 'ID'       , 'BRACKET_ID'  , 'DBL_BRACKET_ID' , 'CURLY_ID' ,
               'ANGLE_ID' , 'NUM'         , 'OPTS_STR'       , 'SPECIAL'  ,
               'TICK'     , 'EMPTY_ANGLE' ] + keyword_tokens

    literals = r"-+*/^|.()\[\]{}=,"

    states = (('input', 'inclusive'),)

    Identifier = '[A-Za-z]([A-Za-z0-9_]*[A-Za-z0-9])?'
    WS         = '[ \t\r\n]'

    t_ignore = ' \t\r'

    def __init__(self):
        self.lexer = []
        self.filename = None
        self.MAX_INPUT_DEPTH = 6

    def t_comment(self, t):
        r'[%#].*'
        pass

    def t_newline(self, t):
        r'\n'
        t.lexer.lineno += 1

    def t_OPTS_STR(self, t):
        r'\[[^\]=]+=[^\]]+\]'
        # [<stuff>=<stuff>]
        t.value = t.value[1:-1]
        return t

    @TOKEN(r"'" + WS + r"*[xyz]")
    def t_TICK(self, t):
        # set the index value
        t.value = "xyz".index(t.value[1])
        return t

    @TOKEN(r'(([0-9]+\.[0-9]*)|(\.[0-9]+)|([0-9]+))([eE][-+]?[0-9]+)?')
    def t_NUM(self, t):
        t.value = float(t.value)
        return t

    def _update_lineno(self, t):
        t.lineno += t.value.count('\n')

    @TOKEN(r'input' + WS + r'*')
    def t_input(self, t):
        self._update_lineno(t)
        t.lexer.begin("input")

    @TOKEN(r'special' + WS + r'*')
    def t_SPECIAL(self, t):
        # TODO(david): add a warning
        self._update_lineno(t)
        return t

    @TOKEN(Identifier)
    def t_ID(self, t):
        t.type = self.reserved.get(t.value, 'ID')
        return t

    @TOKEN(r'<' + Identifier + r'>')
    def t_ANGLE_ID(self, t):
        # strip the brackets off
        t.value = t.value[1:-1]
        return t

    @TOKEN(r'<>')
    def t_EMPTY_ANGLE(self, t):
        return t

    @TOKEN(r'\[' + Identifier + r'\]')
    def t_BRACKET_ID(self, t):
        t.value = t.value[1:-1]
        return t

    @TOKEN(r'\[\[' + Identifier + r'\]\]')
    def t_DBL_BRACKET_ID(self, t):
        t.value = t.value[2:-2]
        return t

    @TOKEN(r'\{' + Identifier + r'\}')
    def t_CURLY_ID(self, t):
        t.value = t.value[1:-1]
        return t

    # Input
    def t_input_FILENAME(self, t):
        r'''\{[^}]*\}'''
        buf = ""
        if self.filename:
            buf = os.path.split(self.filename)[0] + os.sep
        buf += t.value[1:-1] # cut off the braces

        if len(self.lexer) < self.MAX_INPUT_DEPTH:
            with open(buf, 'r') as f:
                # create a new lexer with the same build
                self.lexer.append(self.lexer[-1].clone())
                self.lexer[-1].input(f.read())
                self.lexer[-1].prev_filename = self.filename
                # holds onto the state from last lexer (input)
                self.lexer[-1].begin('INITIAL')
                # stops returning tokens if nothing comes out of this
                return self.lexer[-1].token()
        # ensure lexer is in the right state when popping back
        t.lexer.begin('INITIAL')

    def t_error(self, t):
        print("illegal character: '%s'" % t.value[0])
        t.lexer.skip(1)

    def t_eof(self, t):
        if len(self.lexer) == 1:
            return None
        # remember that last file name and pop back out
        self.filename = self.lexer[-1].prev_filename
        self.lexer.pop()
        # return the next token to make sure we keep going
        return self.lexer[-1].token()

    # build the lexer
    def build(self, **kwargs):
        self.lexer.append(lex.lex(module=self, **kwargs))
        return self

    def input(self, s):
        self.lexer[-1].input(s)

    def token(self):
        return self.lexer[-1].token()

    def __iter__(self):
        return self

    def next(self):
        t = self.token()
        if t is None:
            raise StopIteration
        return t

    __next__ = next

if __name__=="__main__":
    lexer = Lexer().build()
    lex.runmain(lexer)

