
# -*- coding: utf-8 -*-

import json
import geojson

from   django.contrib.auth.decorators import login_required
from   web.lib.decor                  import decor_json, decor_required_ajax, decor_log_request, decor_required_superuser

from   lib.db.const.const_connect     import CONNECT
from   lib.db.const.const_dat         import DAT_REL
from   lib.db.connect.connect_mysql   import DB_read_lines as DB_read_lines_mysql



########################################################
@login_required(login_url='/auth/login/')
@decor_required_ajax
@decor_log_request
@decor_json
def aj_panorama_get(request):
    print(11111)
    return [1,2,5]
    # features  = []
    # param     = json.loads(request.body)
    # # param_key = param.get('key', 1)
    # # param_val = param.get('val', 1)

    # for item in DB_read_lines_mysql(
    #     sql =
    #         "SELECT "+
    #             DATA_FILE_OBJ.TABLE+"."+DATA_FILE_OBJ.ID       +", "+
    #             DATA_FILE_OBJ.TABLE+"."+DATA_FILE_OBJ.PATH+", "+
    #             "ST_AsGeoJSON(PointFromText(CONCAT("+
    #                 "'POINT(',"+
    #                 DATA_POINT_OBJ.TABLE+'.'+DATA_POINT_OBJ.LON+","+
    #                 "' ',"+
    #                 DATA_POINT_OBJ.TABLE+'.'+DATA_POINT_OBJ.LAT+","+
    #                 "')"+
    #             "'),1)) AS location "+
    #         "FROM "+
    #             DAT_REL_COL.TABLE+" "+
    #             "INNER JOIN "+DAT_REL_ROW.TABLE+" "+
    #                 "USING ("+DAT_REL_COL.ID+") "+
    #             "INNER_JOIN "+DATA_FILE_OBJ.TABLE+" "+
    #                 "ON "+DAT_REL_ROW.TABLE+"."+DAT_REL_ROW.REL_ID+"="+
    #                       DATA_FILE_ROW.TABLE+"."+DATA_FILE_OBJ.ID+" "+
    #         "WHERE "+
    #             DAT_REL_COL.TABLE+"."+DAT_REL_COL.KEY_ID+"=1 AND "+
    #             DAT_REL_ROW.TABLE+"."+DAT_REL_ROW.REL_TABLE+"=4"+
    #         "",
    #     database=CONNECT.DATA):
    #     print(item)
    # #     feature  = geojson.Feature(
    # #         id         = str(item[0]),
    # #         properties = { 'address': item[1], },
    # #         geometry   = json.loads(item[2]),
    # #     )
    # #     features.append(feature)
    # # return geojson.FeatureCollection(features)

