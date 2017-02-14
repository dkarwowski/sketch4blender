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

    state = (('input', 'exclusive'),)

    Identifier = '[A-Za-z]([A-Za-z0-9_]*[A-Za-z0-9])?'
    WS         = '[ \t\r\n]'

    t_ignore = ' \t\r'

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

    @TOKEN(r'input' + WS + r'*')
    def t_input(self, t):
        # TODO(david): set up stack frame to parse into
        raise NotImplementedError("need to recurse into file")
        pass

    def _update_lineno(self, t):
        t.lineno += sum([1 for c in t.value if c == '\n'])

    @TOKEN(r'special' + WS + r'*')
    def t_SPECIAL(self, t):
        # TODO(david): add a warning
        _update_lineno(self, t)
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

    def t_error(self, t):
        print("illegal character: '%s'" % t.value[0])
        t.lexer.skip(1)

    def t_eof(self, t):
        return None

    # build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer

if __name__=="__main__":
    lexer = Lexer().build()
    lex.runmain(lexer)

