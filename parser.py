from io import TextIOWrapper
import pathlib
import pprint
import re
from search_regex.mssql import FindSP, GetAttrs


def find_base_text(string):
    clear = lambda x: re.sub(FindSP.DEFAULT, "", x)

    if isinstance(string, str):
        string = clear(string)
    elif isinstance(string, TextIOWrapper):
        string = clear(string.read())
    else:
        raise TypeError(f"Text {type(string)} should be type str or TextIOWrapper")

    text_lines = string.split('\n')

    proc_start = False
    proc_text = ''
    variable_identifier = FindSP.VARIABLE_START_WITH
    start_proc_regex = FindSP.FIND_START
    end_proc_regex = FindSP.FIND_END
    for row in text_lines:
        start = re.search(start_proc_regex, row)
        if start:
            if variable_identifier in row:
                row = row.replace(variable_identifier, f'\n{variable_identifier}')
            proc_text += row + '\n'
            proc_start = True
        param = re.search(variable_identifier, row)
        if proc_start and param:
            proc_text += row + '\n'
        elif proc_start and re.search(end_proc_regex, row):
            if variable_identifier in proc_text:
                return re.sub(FindSP.CLEAR_TRASH, '', proc_text)


def get_attributes(sp_text):
    if isinstance(sp_text, str):
        attrs = {'variables': {}}
        for row in sp_text.split('\n'):
            proc: list = GetAttrs.FIND_NAME.parseString(row)
            if proc:
                proc_name_index = 1
                proc_type = 0
                attrs[proc[proc_type]] = proc[proc_name_index]
                continue
            variable: list = GetAttrs.FIND_ATTRS.parseString(row)
            if variable:
                name_index = 0
                type_index = 1
                variable_name = variable[name_index]
                variable_type = variable[type_index]
                if not variable_name.startswith(FindSP.VARIABLE_START_WITH):
                    continue
                attrs['variables'][variable_name] = {'type': None, 'default': ''}
                try:
                    first_part_type = 2
                    second_part_type = 0
                    default_value = 3
                    if variable[first_part_type][second_part_type].isdigit():
                        variable_type = variable_type + variable[first_part_type]
                        default = variable[default_value]
                    else:
                        default = variable[default_value]
                except IndexError:
                    default_value_identifier = '='
                    if default_value_identifier in variable_type:
                        values = variable_type.split(default_value_identifier)
                        variable_type = values[0]
                        default = values[1]
                    else:
                        default = ''
                clear = lambda x: x.strip(',').strip(';')
                attrs['variables'][variable_name]['type'] = clear(variable_type)
                attrs['variables'][variable_name]['default'] = clear(default)

        return attrs


string = [
    """
    ALTER PROCEDURE dbo.support_LoginAddApi
        @Name			dbo.string = ''
      , @SysName		dbo.string = '' output
      , @Password		dbo.string = '' output
      , @ContractID     dbo.BIDENT
      , @WorkPlaceID    dbo.BIDENT = null
      , @Email			dbo.string = null
      , @ManagerAppUserID dbo.BIDENT = null
      , @WebGate        int = 0
      , @Demo			int = 1
      , @ReGrant        int = 1
      , @ShowResult     int = 1
      , @Ord int = 1
    """,
    """
    ALTER PROCEDURE dbo.GeoPointAdd
      @ID bigint OUTPUT
    , @Latitude numeric(9, 6)
    , @Longitude numeric(9, 6)
    , @SysName varchar(200) = NULL
    , @Name varchar(200) = NULL
    , @Descript varchar(8000) = NULL
    , @OwnerObjectID bigint
    """,
    """
    ALTER PROCEDURE dbo.GetStatisticForBodyWeightScannerBuffer
(	 @Barcode varchar(50)=null--='%101%26079920'
    ,@Name varchar(50)=null--='11363768-0001-1'
    ,@startdate datetime=null
    ,@enddate datetime=null
)
    """,
    """ALTER PROCEDURE dbo.CourierTaskLstForDocumentsCourierRoutingSheet 
    @ID dbo.BIDENT"""
]
# for _ in string:
#     text = find_base_text(_)
#     pprint.pprint(get_attributes(_))

types = []
for file in pathlib.Path('PVZ').iterdir():
    with file.open(mode='r', errors='ignore', encoding='utf-8') as text:
        base_text = find_base_text(text)
        attrs = get_attributes(base_text)
        if attrs:
            for v in attrs['variables'].values():
                if str(v['type']).startswith('@'):
                    print(base_text)
                    pprint.pprint(attrs)
                types.append(re.sub(r'(\(.*\))|\)', '', v['type']))

pprint.pprint(set(types))

# with pathlib.Path('result.sql').open(mode='w', errors='ignore', encoding='utf-8') as res_file:
#     res_file.writelines(result)
