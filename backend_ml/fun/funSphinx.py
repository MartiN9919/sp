
import MySQLdb, MySQLdb.cursors, gc, time
import fun.funSys, fun.funBDNod
from   fun.funConst import SPHINX, IARC, IREL



###################################################################################
#  ЧИТАЕТ РЕЗУЛЬТАТЫ ЗАПРОСА ПО СТРОКАМ (ГЕНЕРАТОР)
###################################################################################
class SphinxReadLines(object):
    def __init__(self, sql, block_size=1000, dataOnServer=True):
        self.db           = sphinxConnect(dataOnServer=dataOnServer)
        self.sql          = sql
        self.block_size   = block_size
        self.dataOnServer = dataOnServer

    def __del__(self):
        sphinxDisconnect(self.db)

    def __iter__(self):
        icount = 3
        while icount>0:
            try:
                self.db.commit()
                cursor = self.db.cursor()
                cursor.execute(self.sql)
                break
            except Exception as e:
                self.db = sphinxReconnect(db=self.db, dataOnServer=self.dataOnServer)
                icount -= 1

        if icount==0: raise Exception('Wrong execute sql: '+self.sql)

        #for row in cursor: yield row
        while True:
            rows = cursor.fetchmany(self.block_size)
            if not rows: break
            for row in rows: yield row




#####################################################
# КЛАСС РАБОТЫ СО SPHINX
#####################################################
class SQL_sphinx():
    def __init__(self):
        self.sphinx = sphinxConnect()

    def __del__(self):
        sphinxDisconnect(self.sphinx)

    def execute(self, sql, wait=False):
        return sphinxSQL(sql, wait, self.sphinx)



#===============================================================================
#   УСТАНОВИТЬ / РАЗОРВАТЬ СОЕДИНЕНИЕ
#===============================================================================
def sphinxConnect(dataOnServer=False):
    return MySQLdb.connect(host=SPHINX.HOST, port=SPHINX.PORT, charset=SPHINX.CHARSET,
                           cursorclass=MySQLdb.cursors.SSCursor if dataOnServer else MySQLdb.cursors.Cursor)

def sphinxDisconnect(db):
    try:
        db.close()
        gc.collect()
    except Exception:
        pass

def sphinxReconnect(db, dataOnServer=False):
    sphinxDisconnect(db)
    iErr = 0
    while True:
        try:
            ret = sphinxConnect(dataOnServer=dataOnServer)
            break
        except Exception as e:
            if (iErr < 10):
                iErr += 1                                                   # ошибка + 1
            else:
                fun.funSys.logger.warning(str(e))                           # вывести сообщение если 10 и более ошибок
                iErr = 0                                                    # обнулить счетчик ошибок
    return ret

def sphinxTables(db=-1):                                                    # список таблиц (индексов) Sphinx
    ret = []
    for item in sphinxSQL(sql='SHOW TABLES', db=db):
        ret.append(item[0].lower())
    return ret


def sphinxValidate(sql, db=-1):                                             # принадлежность запроса к Sphinx - ТОЛЬКО ДЛЯ ПРОСТЫХ ЗАПРОСОВ (FROM ...)
    ret = False
    sql = sql.lower()
    for item in sphinxTables(db=-1):
        if sql.find('from '+item) != -1:
            ret = True
            break
    return ret



#####################################################
# SPHINX: выполнить SQL
# !!!!!! ОБЪЕДИНИТЬ С dbSQL !!!!!!!
#####################################################
# dat  - В МОЕЙ ВРЕМЕННОЙ ЗОНЕ (GMT + UTC)
#####################################################
# sql  - запрос, должен содержать 'commit;' при записи в БД
# wait - ожидать доступности БД
# db   - для работы с открытой базой данных (не обязательно)
#####################################################
#import fun.funDecor
#from atlas.settings import logger
#@fun.funDecor.decorTimer
def sphinxSQL(sql, wait=False, db=-1):

    def run(db, dbOpened, dbReconnect):
        if ((not dbOpened) or dbReconnect): db = sphinxConnect()
        cursor = db.cursor()
        cursor.execute(sql)
        ret = cursor.fetchall()
        cursor.close()
        if not dbOpened: sphinxDisconnect(db)
        return ret

    #logger.info(sql)
    ret = []
    #fun.funSys.logger.info(sql)
    if sql == '': return []
    dbOpened    = (db != -1)
    dbReconnect = False
    iErr        = 0
    while True:
        try:
            ret  = run(db, dbOpened, dbReconnect)
            isOk = True
            #fun.funSys.logger.debug("OK "+sql[:130])
        except Exception as e:                                      # except (MySQLdb.Error, Exception) as e:
            ret  = []
            isOk = not wait
            if (iErr < 10) and wait:
                iErr += 1                                           # ошибка: iErr + 1
            else:
                fun.funSys.logger.warning(str(e)+"\n"+sql[:500])    # вывести сообщение если 10 и более ошибок
                iErr = 0                                            # обнулить счетчик ошибок
        if isOk: break
        dbReconnect = True
        time.sleep(3.0)
    return ret

# плюс описание полей
# ret = {val: (), desc: ()}
def sphinxSQLFull(sql, wait=False, db=-1):

    def run(db, dbOpened, dbReconnect):
        if ((not dbOpened) or dbReconnect): db = sphinxConnect()
        cursor = db.cursor()
        cursor.execute(sql)
        ret = {'val': cursor.fetchall(), 'desc': cursor.description }
        cursor.close()
        if not dbOpened: sphinxDisconnect(db)
        return ret

    #logger.info(sql)
    ret = {'val': (), 'desc': (), 'error': True, 'error_message': 'undefined error'}
    #fun.funSys.logger.info(sql)
    if sql == '': return ret
    dbOpened    = (db != -1)
    dbReconnect = False
    iErr        = 0
    while True:
        try:
            ret  = run(db, dbOpened, dbReconnect)
            isOk = True
            #fun.funSys.logger.debug("OK "+sql[:130])
        except Exception as e:                                      # except (MySQLdb.Error, Exception) as e:
            isOk = not wait
            if (iErr < 10) and wait:
                iErr += 1                                           # ошибка: iErr + 1
            else:
                ret['error_message'] = str(e)
                fun.funSys.logger.warning(str(e)+"\n"+sql[:500])    # вывести сообщение если 10 и более ошибок
                iErr = 0                                            # обнулить счетчик ошибок
        if isOk: break
        dbReconnect = True
        time.sleep(3.0)
    return ret



################################################################################
#   ПОЛУЧИТЬ СНИППЕТЫ
################################################################################
def sphinxSnippetsNod(text, db=-1):
  return sphinxSnippets(text, fun.funBDNod.nodHash.val, db)

def sphinxSnippets(text, nod, db=-1):
    sql = \
        "CALL SNIPPETS( "+ \
            "'"+text+"', "+ \
            "'"+IARC.TABLE_MAIN+"', "+ \
            "'"+nod+"', "+ \
            "5 AS around, "+ \
            "200 AS limit, "+ \
            "1 AS query_mode"+ \
        ")"
    ret = sphinxSQL(sql, False, db)
    return ret[0][0] if len(ret)>0 else text



#####################################################
#   СТРОКА ДЛЯ SPHINX MATCH
#####################################################
#   БЕЗ ЛИШНИХ СИМВОЛОВ (В Т.Ч. ВЫЗЫВАЮЩИХ ОШИБКИ)
#   БЕЗ ЛИШНИХ ПРОБЕЛОВ
#   ОГРАНИЧЕНИЕ ДЛИНЫ (СЛОВА НЕ РАЗБИВАЮТСЯ)
#   БЕЗ ПОСЛЕДНЕГО СЛОВА ПРИ ОБЩЕЙ ДЛИНЕ > 50 (МОЖЕТ БЫТЬ ОБРЕЗАНО РАНЕЕ)
#####################################################
#def sphinxMatch(text, length=150):
#    ret  = ''
#    for item in re.sub(r'[^\w\s]', ' ', text).split(' '):
#        if len(ret) > length: break
#        if len(item)>3: ret+=' '+item
#    return ret.lstrip()





'''
# работает, но не нужна
#===============================================================================
#=====   SPHINX: выборка   =====================================================
#===============================================================================
def sphinxSelect(sMatch='', # параметры Match
                 sFind='', # остальные параметры
                 recFirst=0, # первая возвращаемая запись c 0
                 recCount=300, # количество возвращаемых записей
                 sortField=IARC.DATE, # сортируемое поле
                 sortDirectionAsc=False): # направление сортировки

    # инициализация
    recEnd = recFirst + recCount - 1

    if sFind != '': sFind0 = ' AND '+sFind
    else: sFind0 = sFind

    # сортировка
    sort = sortField
    if sort != '':
        sort = ' ORDER BY '+sort+' '
        if sortDirectionAsc: sort += 'ASC'
        else: sort += 'DESC'
        if sortField != IARC.DATE:
            sort += ', '+IARC.DATE+' DESC'

    # получаем данные
    sql = "SELECT "+IARC.ID+", "+ \
                    IARC.DATE+", "+ \
                    IARC.HOST+", "+ \
                    IARC.SOURCE+", "+ \
                    IARC.TITLE_NAME+", "+ \
                    IARC.AUTHOR_NAME+", "+ \
                    IARC.CONTENT+", "+ \
                    IARC.SNIPPET+"("+IARC.CONTENT+", '"+ \
                        sMatch+"', "+ \
                            "'query_mode=1', "+ \
                            "'limit=400', "+ \
                            "'before_match=<strong>', "+ \
                            "'after_match=</strong>', "+ \
                            "'around=8'"+ \
                        ") AS "+IARC.SNIPPET+", "+ \
                    IARC.EMOTION+" "+ \
            "FROM "+IARC.TABLE+" "+ \
            "WHERE MATCH('"+sMatch+"')"+sFind0+sort+" "+ \
            "LIMIT "+str(recEnd+1)+" "+ \
            "OPTION field_weights=("+IARC.TITLE_NAME+"=100, "+ \
                                     IARC.CONTENT+"=1)"
    data = sphinxSQL(sql)

    # обрезаем ненужные записи с начала
    if recFirst > 0:
        if recFirst < len(data): data = data[recFirst:]
        else: data = []
    return data
'''



'''

function TAtlasMethods.PAGE_Get(const SID, SFind: String): String;
var LSnip, LFind, LNod : TStringList;
    INod               : Integer;

    {Добавление сниппетов от Sphinx}
    procedure SnipAdd_(const SParam: String);
    var J            : TJSONArray;
        IFind, ISnip : Integer;
        SVal         : String;
    begin
        For IFind := 0 to LFind.Count-1 do begin
           J := SNIP_Get_Step(SID, LFind[IFind], SParam);
           For ISnip := 0 to J.Count-1 do begin
              SVal := J.Items[ISnip].Value;
              If LSnip.IndexOf(SVal) < 0 then
                 If Length(SVal) > 3 then LSnip.Add(SVal);
           end;
           J.Free;
        end;
    end;

    {Добавление сниппетов}
    procedure SnipPrepare_(const Str: String);
    var S, S0: String;
    begin
        {Добавление фраз в кавычках}
        S  := Str;
        S0 := BlockCut(S, '"', '"');
        While S0 <> '' do begin
           If LFind.IndexOf(S0) < 0 then LFind.Add(S0);
           If LSnip.IndexOf(S0) < 0 then LSnip.Add(S0);
           S0 := BlockCut(S, '"', '"');
        end;

        {Добавление отдельных слов}
        S := StringReplace(S, '|', ' ', [rfReplaceAll, rfIgnoreCase]);
        S := StringReplace(S, '&', ' ', [rfReplaceAll, rfIgnoreCase]).Trim;
        S0 := TokChar(S, ' ');
        While S0 <> '' do begin
           If Copy(S0, 1, 1) <> '-' then begin
              If LFind.IndexOf(S0) < 0 then LFind.Add(S0);
              If LSnip.IndexOf(S0) < 0 then LSnip.Add(S0);
           end;
           S0 := TokChar(S, ' ');
        end;
    end;

    {Наложение сниппетов на текст}
    function SnipLayer_(const SText, STegBegin, STegEnd: String): String;
    var ISnip, JPos, JStart : Integer;
        S                   : String;

        function Verify(const SText: String): Boolean;
        var ILen: Integer;
        begin
            Result := true;
            ILen   := Length(STegBegin);
            If JPos < ILen then Exit;
            Result := not AnsiSameStr(STegBegin, Copy(SText, JPos-ILen, ILen));
        end;

    begin
        Result := SText;
        LSnip.Sort;
        For ISnip := LSnip.Count-1 downto 0 do begin
           S      := AnsiLowerCase(LSnip[ISnip]);
           JStart := 1;
           JPos   := Pos(S, AnsiLowerCase(Result), JStart);
           While JPos > 0 do begin
              {Не допускаем тэг в тэге}
              If Verify(Result) then begin
                 {Вставка тэга}
                 Insert(STegEnd,   Result, JPos+Length(S));
                 Insert(STegBegin, Result, JPos);
                 JStart := JPos + Length(STegBegin+S+STegEnd);
              end else begin
                 JStart := JPos + Length(S);
              end;
              {Следующее совпадение}
              JPos   := Pos(S, AnsiLowerCase(Result), JStart);
           end;
        end;
    end;


begin
    LFind := TStringList.Create; LFind.CaseSensitive := false;
    LSnip := TStringList.Create; LSnip.CaseSensitive := false;
    LNod  := TStringList.Create; LNod .CaseSensitive := false;
    try
       {Добавление сниппетов}
       SnipPrepare_(SFind);

       {Добавление сниппетов от Sphinx}
       SnipAdd_(SNIPPET_CONTENT);
       SnipAdd_(SNIPPET_PAGE);

       {Наложение на текст сниппетов}
       Result := SnipLayer_(SNIP_Correct(ARC_GetField(SID, F_ARC_CONTENT)), TEG_B_BEGIN, TEG_B_END);
       LFind.Clear;
       LSnip.Clear;

       {*** Наложение на текст объектов интереса ******************************}
       With TADOQuery.Create(Self) do begin
          try
             CursorType := ctOpenForwardOnly;
             LockType   := ltReadOnly;
             Connection := Atlas.BD;
             SQL.Text   := 'SELECT DISTINCT '+T_NOD+'.'+F_NOD_STR+' AS '+F_NOD_STR+' '+
                           'FROM (' +T_NOD+' INNER JOIN '+T_REL+' ON '+T_NOD+'.'+F_NOD_ID    +' = '+T_REL+'.'+F_REL_NOD_ID+')'+
                                           ' INNER JOIN '+T_ARC+' ON '+T_REL+'.'+F_REL_ARC_ID+' = '+T_ARC+'.'+F_ARC_ID    +' '+
                  'WHERE ('+T_ARC+'.'+F_ARC_ID     +'='+SID+') '+
                    'AND ('+T_NOD+'.'+F_NOD_ACTIVE +'=1) '+
                    'AND ('+T_NOD+'.'+F_NOD_USER_ID+'='+SESSION_USER_ID+');';
             Open;
             First;
             While not Eof do begin
                LNod.Add(Fields[0].AsString);
                Next;
             end;
          finally
             Active := false;
             Free;
          end;
       end;

       {Добавление сниппетов}
       For INod := 0 to LNod.Count-1 do SnipPrepare_(LNod[INod]);

       {Добавление сниппетов от Sphinx}
       SnipAdd_(SNIPPET_CONTENT);
       SnipAdd_(SNIPPET_PAGE);

       {Наложение на текст объектов интереса}
       Result := SnipLayer_(Result, TEG_NOD_BEGIN, TEG_NOD_END);
    finally
       LNod.Free;
       LSnip.Free;
       LFind.Free;
    end;

end;

'''


