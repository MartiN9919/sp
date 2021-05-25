ENVIRONMENT_VARIABLES = [
    "PATH",
    "SYSTEM",
    "BYTE",
    "import"
]

IMPORTS = "from   lib.db.io.io               import io_set, io_get_obj, io_get_rel, io_get_geometry_tree\n" \
          "from   lib.db.obj                 import obj_list, key_list, rel_rec_to_el, el_to_rec_id\n" \
          "from   lib.db.geo                 import rel_to_geo_fc, geo_id_to_fc\n\n"

ENABLED_FUNCTIONS = [
    'io_set',
    'io_get_obj',
    'io_get_rel',
    'io_get_geometry_tree',
    'obj_list',
    'key_list',
    'rel_rec_to_el',
    'el_to_rec_id',
    'rel_to_geo_fc',
    'geo_id_to_fc'
]