import pprint
import chevron
import inflection
from typing import List, Optional, Any, AnyStr
from lst.lst import pvz_types, dbo_types

c = {'PROCEDURE': 'dbo.support_LoginAddApi',
     'variables': {'@ContractID': {'default': '', 'type': 'dbo.BIDENT'},
                   '@Demo': {'default': '1', 'type': 'int'},
                   '@Email': {'default': 'null', 'type': 'dbo.string'},
                   '@ManagerAppUserID': {'default': 'null', 'type': 'dbo.BIDENT'},
                   '@Name': {'default': "''", 'type': 'dbo.string'},
                   '@Ord': {'default': '1', 'type': 'int'},
                   '@Password': {'default': "''", 'type': 'dbo.string'},
                   '@ReGrant': {'default': '1', 'type': 'int'},
                   '@ShowResult': {'default': '1', 'type': 'int'},
                   '@SysName': {'default': "''", 'type': 'dbo.string'},
                   '@WebGate': {'default': '0', 'type': 'int'},
                   '@WorkPlaceID': {'default': 'null', 'type': 'dbo.BIDENT'}}}
requiredParams = {'allParams': [{'paramName': '@ContractID'}, {'paramName': '@Demo'}]}


def type_map(sql_type: str):
    sql_type = sql_type.lower()
    int_types = ['int', 'bident', 'bool', 'bit', 'numeric', 'decimal']
    list_types = ['lst', 'list']
    str_types = ['str', 'nvarchar', 'char', 'varchar']

    for i in int_types:
        for l in list_types:
            if i in sql_type and l not in sql_type:
                return 'int'
            elif (i in sql_type and l in sql_type) or 'idlist' in sql_type:
                return 'List[int]'

    for s in str_types:
        for l in list_types:
            if s in sql_type and l not in sql_type:
                return 'str'
            elif s in sql_type and l in sql_type:
                return 'List[str]'

    for l in list_types:
        if l in sql_type:
            return 'list'

    if 'float' in sql_type:
        return 'float'

    return 'Any'


for i in dbo_types:
    print('%s -> %s' % (i, type_map(i)))

# def map_python_param(c):
#     map_attr = {}
#     map_attr['PROCEDURE'] = c['PROCEDURE']
#     map_attr['python_function'] = inflection.underscore(c['PROCEDURE'].replace('.', '_'))
#     map_attr['variables'] = []
#     for variable_name, variable_value in c['variables'].items():
#         sql_name = variable_name
#         python_name = inflection.underscore(variable_name.replace('@', ''))
#
#         dict(sql_name=variable_name)
#         print(map_attr)


# map_python_param(c)

# d = {}
# d['PROCEDURE'] = c['PROCEDURE']
# d['variables'] = [{'name': f'{_} = {inflection.underscore(_[1:])}'} for _ in c['variables'].keys()]
#
# a = """
#     def {{ PROCEDURE }}(
#         self,
#         {{#variables}}
#         {{name}},
#         {{/variables}}
#     ):
#         article_ids = self.client.ids_to_id_list(article_ids)
#         query = f'''
#         SET NOCOUNT ON;
#         EXEC {{ PROCEDURE }}
#         {{#variables}}
#         {{name}},
#         {{/variables}}
#         '''
#         logging.debug(query)
#         dataframe = self.client.dataset_to_dataframe(query)
#         if commit:
#             self.client.cursor.commit()
#         return dataframe
# """
# s = chevron.render(a, d)
# print(s)
#
# a = """
# Hello {{name}}
# You have just won {{value}} dollars!
# {{#in_ca}}
# Well, {{taxed_value}} dollars, after taxes.
# {{/in_ca}}
# Given the following hash:
# """
#
# c = {
#     "name": "Chris",
#     "value": 10000,
#     "taxed_value": 10000 - (10000 * 0.4),
#     "in_ca": False
# }
# # s = chevron.render(a, c)
# # print(s)
#
# a = """
# {{#repo}}
#   <b>{{name}}</b>
# {{/repo}}
# Hash:
# """
#
# c = {
#     "repo": [
#         {"name": "resque"},
#         {"name": "hub"},
#         {"name": "rip"}
#     ]
# }
# s = chevron.render(a, c)
# print(s)
