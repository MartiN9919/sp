from data_base_driver.input_output.input_output import io_get_rel

def trigger_2(group_id, object_id, rec_id, params):
	nums_rels = params.get('nums_rels')
	list = params.get('list')
	rels = io_get_rel(group_id, [50125], [object_id, rec_id], [45], [], {}, True)
	if len(rels) >= int(nums_rels):
	    return True
	else:
	    return False
