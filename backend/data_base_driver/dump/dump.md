## DUMP_OBJ: КЛАССИФИКАТОР ОБЪЕКТОВ


## DUMP_KEY: КЛАССИФИКАТОР КЛЮЧЕЙ
* owners - словарь индексов групп-владельцев owner_id: = {10: [10000, 10001, 10002, 10003], ... }


## DUMP_OWNER: ДОСТУП ВЛАДЕЛЬЦЕВ К ДАННЫМ

### self.dump_users - список пользователей
    * **DAT_OWNER_USERS.ID**
    * **DAT_OWNER_USERS.OWNER_GROUPS_ID**


### self.dump_groups - словарь словарей
    * **DAT_OWNER_GROUPS.ID**        - ID группы
    * **DAT_OWNER_GROUPS.OWNER_LINES_ID** - индекс линии, к которой относится группа
    * **DAT_OWNER_GROUPS.TITLE**     - наименование группы
    * **DAT_OWNER_GROUPS.DESCRIPT**  - описание группы, контактные телефоны и т.д.
```python
self.dump_groups = {
 32: {'id': 1, 'title': 'Полоцк А', 'lines': [1],    'groups_rw': [32, 33, 34, 35], 'groups_id': [34]},
 33: {'id': 2, 'title': 'Полоцк О', 'lines': [1, 2], 'groups_ro': [33]},
 34: {'id': 3, 'title': 'Полоцк И', 'lines': [3],    'groups_id': [34]},
}
```


