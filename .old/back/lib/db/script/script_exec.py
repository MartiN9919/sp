# -*- coding: utf-8 -*-

###########################################
# СДЕЛАТЬ
###########################################
# значение аргументов функции по умолчанию. Временно применять конструкцию if not fun_var_exist('where_dop'): where_dop = []
# работа со словарем
# передача в качестве аргументов функции * list или ** dict
###########################################


import re
import json
#import geojson
import copy
#import logging

from   pprint                       import pprint

from   rply                         import LexerGenerator, ParserGenerator
from   rply.token                   import Token

from   lib.const                    import RET_ERROR
from   lib.db.const.const_connect   import CONNECT
from   lib.db.const.const_dat       import DAT_SYS_SCRIPT, DAT_OWNER
from   lib.db.connect.connect_mysql import DB_sql as MYSQL


###########################################
# EXTERNAL FUNCTION
###########################################
from   lib.db.io.io               import io_set, io_get_obj, io_get_rel, io_get_geometry_tree
from   lib.db.obj                 import obj_list, key_list, rel_rec_to_el, el_to_rec_id
from   lib.db.geo                 import rel_to_geo_fc, geo_id_to_fc


DEBUG = False


###########################################
# ВЫПОЛНИТЬ СКРИПТ
###########################################
def script_exec(group_id, var_start):
    if DEBUG: print_var(var_start)
    script_name    = var_start.pop('script')
    script_handler = SCRIPT_EXEC(group_id, var_start=var_start)
    return script_handler.execute(script_name)

class SCRIPT_EXEC():
    def __init__(self, group_id, var_start={}):
        self.group_id = group_id
        self.db       = MYSQL(database=CONNECT.DATA)
        self.lexer    = Lexer().get_lexer()
        self.pg       = Parser(lexer=self.lexer, var_start=var_start, db=self.db)
        self.parser   = self.pg.get_parser()

    def execute(self, script_name):
        script, _  = self.get(script_name)
        script     = re.sub(r'\s*\\\r\n\s*', ' ', script)           # \ new str
        for line in script.split('\r\n'):
            if line.strip() == '': continue
            if DEBUG: print_lexer(self.lexer, line)
            tokens = self.lexer.lex(line)
            if DEBUG: print_parser()
            self.parser.parse(tokens)                               #.eval()
        return self.pg.var.get('ret', None)


    def get(self, script_name, owner=None):
        sql = \
            "SELECT "+\
                DAT_SYS_SCRIPT.CONTENT   +", "+\
                DAT_SYS_SCRIPT.TITLE     +", "+\
                DAT_SYS_SCRIPT.OWNER_LINE+" " +\
            "FROM "  + DAT_SYS_SCRIPT.TABLE_SHORT + " "+ \
            "WHERE " + \
                DAT_SYS_SCRIPT.ENABLED + "=1 AND "+ \
                DAT_SYS_SCRIPT.NAME    + "='" + script_name +"'"
        rec = self.db.execute(sql=sql, wait=not DEBUG, read=True)

        # скрипт: наличие
        if len(rec) != 1:
            raise Exception(RET_ERROR.MSG_RECORD+": '"+script_name+"'")
        # скрипт: доступность
        if not DAT_OWNER.DUMP.valid_line_group(group_id=self.group_id, line_id=rec[0][-1]):   # !!! rec[0][-1]
            raise Exception(RET_ERROR.MSG_RECORD+": '"+script_name+"'")

        return rec[0][0], rec[0][1]



###########################################
# ОБЪЕКТЫ ВСПОМОГАТЕЛЬНЫЕ
###########################################
class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def get_lexer(self):
        self.lexer.add('NULL',            r'\#.*')
        self.lexer.add('IF',              r'(?i)IF(?!\w)')
        self.lexer.add('CONDITION_AFTER', r'\:.*')

        self.lexer.add('MATH_NOT',        r'(?i)NOT(?!\w)')
        self.lexer.add('MATH_LOGIC',      r'(?i)AND|OR(?!\w)')

        #self.lexer.add('FUNCTION',        r'(?i)(?=FUN_)\w+')
        self.lexer.add('FUNCTION',        r'(?i)(?=[a-zA-Z0-9_]+\s*\(.*\))\w+')
        #self.lexer.add('PRINT',           r'(?i)print(?!\w)')

        self.lexer.add('INDEX',           r'[a-zA-Z0-9_]+(\[.+?\])+')                   # dat[key][2][...]
        self.lexer.add('NONE',            r'(?i)none')
        self.lexer.add('FLOAT',           r'\d+\.\d+')
        self.lexer.add('NUMBER',          r'\d+')
        self.lexer.add('STRING',          r'(\"\"\".*?\"\"\")|(\'\'\'.*?\'\'\')|(\".*?\")|(\'.*?\')')
        self.lexer.add('BOOLEAN',         r'(?i)true(?!\w)|false(?!\w)')
        self.lexer.add('IDENTIFIER',      r'[a-zA-Z0-9_]+')
        # self.lexer.add('LIST',            r'\[.*?\]')                                 # не жадный - недопустимо вложение
        # self.lexer.add('DICT',            r'\{.*?\}')                                 # не жадный - недопустимо вложение

        self.lexer.add('(',               r'\(')
        self.lexer.add(')',               r'\)')
        self.lexer.add('[',               r'\[')
        self.lexer.add(']',               r'\]')
        self.lexer.add('MATH_COMPARE',    r'(==)|(!=)|(<>)|(>=)|(<=)|(>)|(<)')          # сначала большей длины
        self.lexer.add('MATH_ACTION1',    r'(\*)|(\/)')
        self.lexer.add('MATH_ACTION2',    r'(\+)|(\-)')

        self.lexer.add('=',               r'\=')
        self.lexer.add(',',               r'\,')

        self.lexer.ignore(r'\s+')                                                       # '\s+'   '[ \t\r\f\v]+'

        return self.lexer.build()


class Parser():
    def __init__(self, lexer, var_start={}, db=-1):
        self.lexer = lexer
        self.db    = db
        self.pg    = ParserGenerator(
            tokens     = [
                'NULL', 'IDENTIFIER', 'STRING', 'NUMBER', 'INDEX', 'NONE', 'FLOAT', 'BOOLEAN', '[', ']', # 'DICT', 'LIST',
                'FUNCTION', 'IF', 'CONDITION_AFTER',
                '(', ')',
                'MATH_COMPARE', 'MATH_ACTION1', 'MATH_ACTION2', 'MATH_LOGIC', 'MATH_NOT',
                '=', ',',
            ],
            precedence = [
                ('left', ['MATH_COMPARE']),
                ('left', ['MATH_ACTION2']),
                ('left', ['MATH_ACTION1']),
                ('left', ['(', ')']),
                ('left', ['[', ']']),

                #('left', ['IDENTIFIER', 'STRING', 'NUMBER', 'INDEX', 'NONE', 'FLOAT', 'BOOLEAN', 'LIST', 'DICT']),
                ('left', ['IDENTIFIER', 'STRING', 'NUMBER', 'INDEX', 'NONE', 'FLOAT', 'BOOLEAN', ]),

                ('left', ['IF', 'CONDITION_AFTER']),
                ('left', ['MATH_LOGIC',]),
                ('left', ['MATH_NOT',]),
            ],
        )

        self.funs = [
            io_set, io_get_obj, io_get_rel, io_get_geometry_tree,
            obj_list, key_list,
            rel_rec_to_el, el_to_rec_id,
            rel_to_geo_fc, geo_id_to_fc,

            self.var_exist,
            self.mysql,
            print,
        ]
        self.funs = { x.__name__: x for x in self.funs }

        # Предустановленные переменные
        self.var = copy.deepcopy(var_start)


        ###########################################
        # EXPRESSION
        ###########################################
        @self.pg.production('expression : NULL')
        def fun_null(p):
            pass

        @self.pg.production('expression : IDENTIFIER')
        def var_identifier(p):
            ret = self.var.get(p[0].value, p[0].value)
            self.print_debug('IDENTIFIER:', p[0].value, '==', str(ret)[:150])
            return Var(ret)

        @self.pg.production('expression : STRING')
        def var_string(p):
            ret = p[0].value
            if len(ret) >= 2: ret = re.sub(r'(^\".*?\"$)|(^\'.*?\'$)',         ret[1:-1], ret)  # удалить крайние кавычки
            if len(ret) >= 4: ret = re.sub(r'(^\"\".*?\"\"$)|(^\'\'.*?\'\'$)', ret[2:-2], ret)
            self.print_debug('STRING:', p[0].value, '=', ret)
            return Var(ret)

        @self.pg.production('expression : NUMBER')
        def var_number(p):
            ret = int(p[0].value)
            self.print_debug('NUMBER:', p[0].value, '=', ret)
            return Var(ret)

        @self.pg.production('expression : BOOLEAN')
        def var_boolean(p):
            ret = len(p[0].value) == 4
            self.print_debug('BOOLEAN:', p[0].value, '=', ret)
            return Var(ret)

        @self.pg.production('expression : NONE')
        def var_none(p):
            self.print_debug('NONE')
            return Var(None)

        @self.pg.production('expression : FLOAT')
        def var_float(p):
            ret = float(p[0].value)
            self.print_debug('FLOAT:', p[0].value, '=', ret)
            return Var(ret)

        # @self.pg.production('expression : LIST')
        # @self.pg.production('expression : DICT')
        # def var_list(p):
        #     val = p[0].value
        #     val = re.sub(r'(?i)true(?!\w)',  'true',  val)                  # в формат JSON
        #     val = re.sub(r'(?i)false(?!\w)', 'false', val)
        #     val = re.sub(r'\'',              '"',     val)
        #     ret = json.loads(val)
        #     self.print_debug('DICT:', ret)
        #     return Var(ret)

        @self.pg.production('expression : [ ]')
        @self.pg.production('expression : [ expression ]')
        @self.pg.production('expression : [ expression , expression ]')
        @self.pg.production('expression : [ expression , expression , expression ]')
        @self.pg.production('expression : [ expression , expression , expression , expression ]')
        @self.pg.production('expression : [ expression , expression , expression , expression , expression ]')
        @self.pg.production('expression : [ expression , expression , expression , expression , expression , expression ]')
        @self.pg.production('expression : [ expression , expression , expression , expression , expression , expression , expression ]')
        def var_list(p):
            ret = [ p[item_param].value for item_param in range(1, len(p)-1, 2) ]
            self.print_debug('LIST:', ret)
            return Var(ret)

        @self.pg.production('expression : INDEX')
        def var_index(p):
            val = p[0].value
            var_nam = re.findall(r'^(.*?)\[', val)[0]
            var_val = self.var[var_nam]
            for item in re.findall(r'\[(.+?)\]', val):
                if item.isnumeric(): item = int(item)
                var_val = var_val[item]
            self.print_debug('INDEX:', val, '=', str(var_val)[:150])
            return Var(var_val)

        @self.pg.production('expression : IDENTIFIER = expression')
        def equ_1(p):
            self.print_debug('IDENTIFIER = expression: ', p[0].value, '=', str(p[2].value)[:150])
            self.var[p[0].value] = p[2].value
            return Var(p[0].value)

        @self.pg.production('expression : ( expression ) ')
        def fun_quotes(p):
            self.print_debug('(', p[1].value, ')')
            return p[1]



        ###########################################
        # MATH
        ###########################################
        @self.pg.production('expression : expression MATH_COMPARE expression ')
        @self.pg.production('expression : expression MATH_ACTION1 expression ')
        @self.pg.production('expression : expression MATH_ACTION2 expression ')
        @self.pg.production('expression : expression MATH_LOGIC   expression ')
        def fun_compare(p):
            operand_1 = p[0].value
            action    = p[1].value
            operand_2 = p[2].value

            if   action == '==':  ret = (operand_1 ==  operand_2)
            elif action == '!=':  ret = (operand_1 !=  operand_2)
            elif action == '<>':  ret = (operand_1 !=  operand_2)
            elif action == '>=':  ret = (operand_1 >=  operand_2)
            elif action == '<=':  ret = (operand_1 <=  operand_2)
            elif action == '>':   ret = (operand_1 >   operand_2)
            elif action == '<':   ret = (operand_1 <   operand_2)

            elif action == '*':   ret =  operand_1 *   operand_2
            elif action == '/':   ret =  operand_1 /   operand_2
            elif action == '+':   ret =  operand_1 +   operand_2
            elif action == '-':   ret =  operand_1 -   operand_2

            elif action == 'and': ret =  operand_1 and operand_2            # lower case
            elif action == 'or':  ret =  operand_1 or  operand_2            # lower case

            else: raise Exception(RET_ERROR.MSG_PARAM+": action='"+str(action)+"'")

            self.print_debug('MATH:', operand_1, action, operand_2, '=', ret)
            return Var(ret)

        @self.pg.production('expression : MATH_NOT expression ')
        def fun_compare(p):
            operand = p[1].value
            ret = not operand
            self.print_debug('MATH_NOT:', operand, '=', ret)
            return Var(ret)



        ###########################################
        # IF
        ###########################################
        @self.pg.production('expression : IF expression CONDITION_AFTER ')
        def fun_if(p):
            prog_if = p[2].value[2:]
            self.print_debug('IF:', p[1].value,)
            if p[1].value: self.exec_subprog(prog_if)



        ###########################################
        # FUNCTION
        ###########################################
        @self.pg.production('expression : FUNCTION  ( )')
        @self.pg.production('expression : FUNCTION  ( expression )')
        @self.pg.production('expression : FUNCTION  ( expression , expression )')
        @self.pg.production('expression : FUNCTION  ( expression , expression , expression )')
        @self.pg.production('expression : FUNCTION  ( expression , expression , expression , expression )')
        @self.pg.production('expression : FUNCTION  ( expression , expression , expression , expression , expression )')
        @self.pg.production('expression : FUNCTION  ( expression , expression , expression , expression , expression , expression )')
        @self.pg.production('expression : FUNCTION  ( expression , expression , expression , expression , expression , expression , expression )')
        def fun_exec(p):
            fun_name  = p[0].value
            fun_param = []
            for item_param in range(2, len(p)-1, 2):
                fun_param.append(p[item_param].value)
            self.print_debug('FUN_RUN:', fun_name, str(fun_param)[:5000])
            ret = self.funs[fun_name](*fun_param)
            self.print_debug('FUN_RET:', str(ret)[:150])
            return Var(ret)



        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()

    # выполнить подпрограмму
    def exec_subprog(self, prog):
        parser = self.get_parser()
        for line in prog.split(';'):
            if line.strip() == '': continue
            if DEBUG: print_lexer(self.lexer, line, ' (subprog)')
            tokens = self.lexer.lex(line)
            if DEBUG: print_parser(title = ' (subprog)')
            parser.parse(tokens)


    def print_debug(self, *args):
        if DEBUG:
            val = list(map(lambda x: str(x), args))
            print(' '.join(val))

    # СУЩЕСТВУЕТ ЛИ ПЕРЕМЕННАЯ
    def var_exist(self, var_name):
        ret = self.var.get(var_name, None) != None
        self.print_debug('VAR_EXIST:', var_name, '=', ret)
        return ret

    # ЗАПРОС К MYSQL.VEC_DATA
    def mysql(self, *args):
        ret = self.db.execute(*args)
        #self.print_debug('SQL:', *args)
        return ret



class Var():
    def __init__(self, value): self.value = value
    def eval(self):            return self.value


def print_var(var, title=''):
    print('\n===== VAR'+title+' =====\n>', var)
def print_lexer(lexer, line, title=''):
    print('===== LEXER'+title+' =====\n>', line, '\n>', list(lexer.lex(line)))
def print_parser(title=''):
    print('===== PARSER'+title+' =====')
