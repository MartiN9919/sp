from   lib.db.io.io               import io_set, io_get_obj, io_get_rel, io_get_geometry_tree
from   lib.db.obj                 import obj_list, key_list, rel_rec_to_el, el_to_rec_id
from   lib.db.geo                 import rel_to_geo_fc, geo_id_to_fc



def script_7(request):
	try:
		keys_rel = request.get('keys_rel',[])
		keys_obj = request.get('keys_obj',[])
		where_dop = request.get('where_dop',[])
		object_name = request.get('object_name',[])
		group_id = 1
		rel_recs = io_get_rel(group_id,keys_rel,[object_name],None,where_dop)
		els = rel_rec_to_el(rel_recs)
		geo_ids = el_to_rec_id(object_name,els)
		ret = geo_id_to_fc(object_name,group_id,geo_ids,keys_obj)
		return ret
	except BaseException:
		return 'error'