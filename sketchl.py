import ply.lex as lex

reserved = {
        'language'   : 'LANGUAGE'   ,
        'pstricks'   : 'PSTRICKS'   ,
        'tikz'       : 'TIKZ'       ,
        'latex'      : 'LaTeX'      ,
        'context'    : 'ConTeXt'    ,
        'curve'      : 'CURVE'      ,
        'camera'     : 'CAMERA'     ,
        'def'        : 'DEF'        ,
        'dots'       : 'DOTS'       ,
        'frame'      : 'FRAME'      ,
        'global'     : 'GLOBAL'     ,
        'line'       : 'LINE'       ,
        'polygon'    : 'POLYGON'    ,
        'put'        : 'PUT'        ,
        'repeat'     : 'REPEAT'     ,
        'set'        : 'SET'        ,
        'sweep'      : 'SWEEP'      ,
        'then'       : 'THEN'       ,
        'picturebox' : 'PICTUREBOX'
}

# TODO(david): remove reserved words from having to be input manually
tokens = ( 'ID'        , 'PAREN_ID'   , 'BRACKET_ID'  , 'DBL_BRACKET_ID' , 'CURLY_ID'    ,
           'ANGLE_ID'  , 'NUM'        , 'OPTS_STR'    , 'SPECIAL'        , 'TICK'        ,
           'THEN'      , 'DEF'        , 'EMPTY_ANGLE' , 'DOTS'           , 'LINE'        ,
           'CURVE'     , 'POLYGON'    , 'REPEAT'      , 'SWEEP'          , 'PUT'         ,
           'TRANSLATE' , 'ROTATE'     , 'SCALE'       , 'PROJECT'        , 'PERSPECTIVE' ,
           'VIEW'      , 'SQRT'       , 'SIN'         , 'ASIN'           , 'COS'         ,
           'ACOS'      , 'ATAN2'      , 'UNIT'        , 'INVERSE'        , 'GLOBAL'      ,
           'SET'       , 'PICTUREBOX' , 'FRAME'       , 'CAMERA'         , 'LANGUAGE'    ,
           'PSTRICKS'  , 'TIKZ'       , 'LaTeX'       , 'ConTeXt'        , 'NEG'         )

state = (('input', 'exclusive'),)

identifier = r'[A-Za-z]([A-Za-z0-9_]*[A-Za-z0-9])?'
ws_not_nl  = r'[ \t\r]'
ws         = r'[ \t\r\n]'

t_ignore = ws_not_nl

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

@TOKEN(identifier)
def t_ID(t):
    t.type = reserved.get(t.value, 'ID')
    return t

@TOKEN(r'input' + ws + r'*')
def t_input(t):
    pass

