## DUMP_OBJ: КЛАССИФИКАТОР ОБЪЕКТОВ


## DUMP_KEY: КЛАССИФИКАТОР КЛЮЧЕЙ
* owners - словарь индексов групп-владельцев owner_id: = {10: [10000, 10001, 10002, 10003], ... }


## DUMP_OWNER: ДОСТУП ВЛАДЕЛЬЦЕВ К ДАННЫМ

### self.dump_users - список пользователей
* **DAT_OWNER_USERS.ID**
* **DAT_OWNER_USERS.OWNER_GROUPS_ID**


### self.dump_groups - словарь словарей
* key 1:
    * **DAT_OWNER_GROUPS.ID**        - ID группы
* key_2:
    * **DAT_OWNER_GROUPS.GROUPS_ID** - список индексов групп, к которым имеет доступ лицо, прикрепленное к группе
    * **DAT_OWNER_GROUPS.TITLE**     - наименование группы
    * **DAT_OWNER_GROUPS.DESCRIPT**  - описание группы, контактные телефоны и т.д.

### функции
* valid_user() - проверить доступ пользователя user_id к данным хотя бы одной из групп valids_id
* valid_group() - проверить доступ группы group_id к данным хотя бы одной из групп valids_id
* get_group() - user_id в group_id

```python
self.dump_groups = {
 25: {'descript': None,
      'groups_id': [65, 35, 105, 75, 45, 115, 85, 55, 25, 125, 95],
      'title': 'ГПКД'},
 32: {'descript': None, 'groups_id': [32, 33, 34, 35], 'title': 'Полоцк А'},
 33: {'descript': None, 'groups_id': [33],             'title': 'Полоцк О'},
 34: {'descript': None, 'groups_id': [34],             'title': 'Полоцк И'},
 35: {'descript': None, 'groups_id': [35],             'title': 'Полоцк Д'},
}
enabled = DAT_OWNER.DUMP.valid_user(user_id=1, valids_id=[44, 45])
```


