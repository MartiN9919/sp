from data_base_driver.sys_key.get_key_dump import get_key_by_id


def validate(record):
    key = get_key_by_id(record['id'])
    print(key)

