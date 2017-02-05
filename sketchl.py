import ply.lex as lex
from ply.lex import TOKEN

keyword_tokens = [ 'LANGUAGE'  , 'PSTRICKS' , 'TIKZ'    , 'LaTeX'      , 'ConTeXt'     ,
                   'CURVE'     , 'CAMERA'   , 'DEF'     , 'DOTS'       , 'FRAME'       ,
                   'GLOBAL'    , 'LINE'     , 'POLYGON' , 'PUT'        , 'REPEAT'      ,
                   'SET'       , 'SWEEP'    , 'THEN'    , 'PICTUREBOX' , 'ASIN'        ,
                   'ACOS'      , 'ATAN2'    , 'COS'     , 'INVERSE'    , 'PERSPECTIVE' ,
                   'PROJECT'   , 'ROTATE'   , 'SCALE'   , 'SIN'        , 'SQRT'        ,
                   'TRANSLATE' , 'UNIT'     , 'VIEW'    ]

reserved = { keyword.lower() : keyword for keyword in keyword_tokens }

# TODO(david): remove reserved words from having to be input manually
tokens = [ 'ID'       , 'BRACKET_ID'  , 'DBL_BRACKET_ID' ,
           'CURLY_ID' , 'ANGLE_ID' , 'NUM'         , 'OPTS_STR'       ,
           'SPECIAL'  , 'TICK'     , 'EMPTY_ANGLE' ] + keyword_tokens

literals = r"-+*/^|.()\[\]{}=,"

state = (('input', 'exclusive'),)

Identifier = '[A-Za-z]([A-Za-z0-9_]*[A-Za-z0-9])?'
WS         = '[ \t\r\n]'

t_ignore = ' \t\r'

def t_comment(t):
    r'[%#].*'
    pass

def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

def t_OPTS_STR(t):
    r'\[[^\]=]+=[^\]]+\]'
    # [<stuff>=<stuff>]
    t.value = t.value[1:-1]
    return t

@TOKEN(r"'" + WS + r"*[xyz]")
def t_TICK(t):
    # set the index value
    t.value = "xyz".index(t.value[1])
    return t

@TOKEN(r'(([0-9]+\.[0-9]*)|(\.[0-9]+)|([0-9]+))([eE][-+]?[0-9]+)?')
def t_NUM(t):
    t.value = float(t.value)
    return t

@TOKEN(r'input' + WS + r'*')
def t_input(t):
    # TODO(david): set up stack frame to parse into
    raise NotImplementedError("need to recurse into file")
    pass

def _update_lineno(t):
    t.lineno += sum([1 for c in t.value if c == '\n'])

@TOKEN(r'special' + WS + r'*')
def t_SPECIAL(t):
    # TODO(david): add a warning
    _update_lineno(t)
    return t

@TOKEN(Identifier)
def t_ID(t):
    t.type = reserved.get(t.value, 'ID')
    return t

@TOKEN(r'<' + Identifier + r'>')
def t_ANGLE_ID(t):
    # strip the brackets off
    t.value = t.value[1:-1]
    return t

@TOKEN(r'<>')
def t_EMPTY_ANGLE(t):
    return t

@TOKEN(r'\[' + Identifier + r'\]')
def t_BRACKET_ID(t):
    t.value = t.value[1:-1]
    return t

@TOKEN(r'\[\[' + Identifier + r'\]\]')
def t_DBL_BRACKET_ID(t):
    t.value = t.value[2:-2]
    return t

@TOKEN(r'\{' + Identifier + r'\}')
def t_CURLY_ID(t):
    t.value = t.value[1:-1]
    return t

def t_error(t):
    print("illegal character: '%s'" % t.value[0])
    t.lexer.skip(1)

def t_eof(t):
    return None

lexer = lex.lex()

if __name__=="__main__":
    lex.runmain()

