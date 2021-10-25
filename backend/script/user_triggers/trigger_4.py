from data_base_driver.input_output.input_output import io_get_rel

def trigger_4(group_id, object_id, rec_id, params):
	nums = params.get('nums')
	rels = io_get_rel(group_id, [3333], [object_id, rec_id], [45], [], {}, True)
	if len(rels) > 5:
	    return True
	else:
	    return False
