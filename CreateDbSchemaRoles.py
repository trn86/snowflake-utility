import sys
import yaml
from CreateWarehouse import create_warehouse
from CreateWarehouseRoleMapping import create_warehouse_role_mapping
from CreateRoleToRoleMapping import create_role_to_role_mapping
from CreateUserToRoleMapping import create_user_role_mapping

def create_db_schema_dictionary():
    dbDict = {}
    with open('mapping.yaml', 'r') as file:
        configyml = yaml.safe_load(file)
        dbDict["db"]= configyml['database']['name']
        lst = []
        for schema in configyml['schemas']:
          lst.append(schema)
        dbDict["schemas"]=lst
        dbDict["db_admin_role"]=configyml['databaseroles']['admin_role']
        dbDict["db_rw_role"]=configyml['databaseroles']['dev_role']
        dbDict["db_ro_role"]=configyml['databaseroles']['analyst_role']
        dbDict["SECURITYADMIN"]='USE ROLE SECURITYADMIN;\n'
        dbDict["SYSADMIN"]='USE ROLE SYSADMIN;\n'
        dbDict["USERADMIN"]='USE ROLE USERADMIN;\n'
        print(dbDict)
    return dbDict

def create_db_schema_roles(dict):
    createRoleString = 'CREATE OR REPLACE ROLE ' if dict['flag'] == 'Create' else 'DROP ROLE '
    createDatabaseString = 'CREATE OR REPLACE DATABASE ' if dict['flag'] == 'Create' else 'DROP DATABASE '
    createSchemaString = 'CREATE OR REPLACE SCHEMA ' if dict['flag'] == 'Create' else ''
    opString = ''
    with open('mapping.yaml', 'r') as file:
        configyml = yaml.safe_load(file)
        opString = dict['SYSADMIN']
        opString = opString + createDatabaseString + dict['db'] + ";\n"
        for schema in dict['schemas']:
          opString = opString + dict['SYSADMIN']
          if dict['flag'] == 'Create':
            opString = opString +  createSchemaString + dict['db'] + "."+ schema + ";\n"
        opString = opString + dict['SECURITYADMIN']
        opString = opString + createRoleString + configyml['databaseroles']['admin_role'] + ";\n"
        opString = opString + createRoleString + configyml['databaseroles']['dev_role'] + ";\n"
        opString = opString + createRoleString + configyml['databaseroles']['analyst_role'] + ";\n"

        opString = opString + createRoleString + configyml['functionalroles']['admin_role'] + ";\n"
        opString = opString + createRoleString + configyml['functionalroles']['dev_role'] + ";\n"
        opString = opString + createRoleString + configyml['functionalroles']['analyst_role'] + ";\n"

        opString = opString + createRoleString + configyml['warehouseroles']['admin_role'] + ";\n"
        opString = opString + createRoleString + configyml['warehouseroles']['dev_role'] + ";\n"
        for role in configyml['serviceintegrationroles']:
          opString = opString + createRoleString + role + ";\n"
    return opString

def create_role_privileges_mapping(dict):
    roleGrantString = ''
    roleGrantString = roleGrantString + create_admin_privileges(dict) + "\n"
    roleGrantString = roleGrantString + create_developer_privileges(dict) + "\n"
    roleGrantString = roleGrantString + create_analyst_privileges(dict) + "\n"
    return roleGrantString

def create_admin_privileges(dict):
    result = dict['SECURITYADMIN']
    result = result + f'''GRANT ALL PRIVILEGES ON DATABASE {dict['db']} TO ROLE {dict['db_admin_role']};\n'''
    for schema in dict['schemas']:
          result = result + f'''GRANT ALL PRIVILEGES ON SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_admin_role']};
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_admin_role']};
GRANT ALL PRIVILEGES ON FUTURE TABLES IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_admin_role']};
GRANT ALL PRIVILEGES ON ALL VIEWS IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_admin_role']};
GRANT ALL PRIVILEGES ON FUTURE VIEWS IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_admin_role']};
GRANT ALL PRIVILEGES ON ALL PROCEDURES IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_admin_role']};
GRANT ALL PRIVILEGES ON FUTURE PROCEDURES IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_admin_role']};
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_admin_role']};
GRANT ALL PRIVILEGES ON FUTURE FUNCTIONS IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_admin_role']};
GRANT ALL PRIVILEGES ON ALL FILE FORMATS IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_admin_role']};
GRANT ALL PRIVILEGES ON FUTURE FILE FORMATS IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_admin_role']};
GRANT ALL PRIVILEGES ON ALL STAGES IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_admin_role']};
GRANT ALL PRIVILEGES ON FUTURE STAGES IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_admin_role']};
GRANT ALL PRIVILEGES ON ALL STREAMS IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_admin_role']};
GRANT ALL PRIVILEGES ON FUTURE STREAMS IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_admin_role']};
GRANT ALL PRIVILEGES ON ALL TASKS IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_admin_role']};
GRANT ALL PRIVILEGES ON FUTURE TASKS IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_admin_role']};
GRANT ALL PRIVILEGES ON ALL EXTERNAL TABLES IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_admin_role']};
GRANT ALL PRIVILEGES ON FUTURE EXTERNAL TABLES IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_admin_role']};
'''
    return result

    
def create_developer_privileges(dict):
    result = dict['SECURITYADMIN']
    result = result + f'''GRANT USAGE ON DATABASE {dict['db']} TO ROLE {dict['db_rw_role']};\n'''
    for schema in dict['schemas']:
          result = result + f'''GRANT USAGE ON SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_rw_role']};
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_rw_role']};
GRANT ALL PRIVILEGES ON FUTURE TABLES IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_rw_role']};
GRANT ALL PRIVILEGES ON ALL VIEWS IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_rw_role']};
GRANT ALL PRIVILEGES ON FUTURE VIEWS IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_rw_role']};
GRANT ALL PRIVILEGES ON ALL PROCEDURES IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_rw_role']};
GRANT ALL PRIVILEGES ON FUTURE PROCEDURES IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_rw_role']};
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_rw_role']};
GRANT ALL PRIVILEGES ON FUTURE FUNCTIONS IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_rw_role']};
GRANT ALL PRIVILEGES ON ALL FILE FORMATS IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_rw_role']};
GRANT ALL PRIVILEGES ON FUTURE FILE FORMATS IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_rw_role']};
GRANT ALL PRIVILEGES ON ALL STAGES IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_rw_role']};
GRANT ALL PRIVILEGES ON FUTURE STAGES IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_rw_role']};
GRANT ALL PRIVILEGES ON ALL STREAMS IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_rw_role']};
GRANT ALL PRIVILEGES ON FUTURE STREAMS IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_rw_role']};
GRANT ALL PRIVILEGES ON ALL TASKS IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_rw_role']};
GRANT ALL PRIVILEGES ON FUTURE TASKS IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_rw_role']};
GRANT ALL PRIVILEGES ON ALL EXTERNAL TABLES IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_rw_role']};
GRANT ALL PRIVILEGES ON FUTURE EXTERNAL TABLES IN SCHEMA {dict['db']}.{schema} TO ROLE {dict['db_rw_role']};
'''
    return result
    
def create_analyst_privileges(dict):
    result = dict['SECURITYADMIN']
    result = result + f'''GRANT USAGE ON DATABASE {dict['db']} TO ROLE DR_RO;\n'''
    for schema in dict['schemas']:
          result = result + f'''GRANT USAGE ON SCHEMA {dict['db']}.{schema} TO ROLE DR_RO;
GRANT SELECT ON ALL TABLES IN SCHEMA {dict['db']}.{schema} TO ROLE DR_RO;
GRANT SELECT ON FUTURE TABLES IN SCHEMA {dict['db']}.{schema} TO ROLE DR_RO;
GRANT SELECT ON ALL VIEWS IN SCHEMA {dict['db']}.{schema} TO ROLE DR_RO;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA {dict['db']}.{schema} TO ROLE DR_RO;
GRANT USAGE ON ALL PROCEDURES IN SCHEMA {dict['db']}.{schema} TO ROLE DR_RO;
GRANT USAGE ON FUTURE PROCEDURES IN SCHEMA {dict['db']}.{schema} TO ROLE DR_RO;
GRANT USAGE ON ALL FUNCTIONS IN SCHEMA {dict['db']}.{schema} TO ROLE DR_RO;
GRANT USAGE ON FUTURE FUNCTIONS IN SCHEMA {dict['db']}.{schema} TO ROLE DR_RO;
GRANT USAGE ON ALL FILE FORMATS IN SCHEMA {dict['db']}.{schema} TO ROLE DR_RO;
GRANT USAGE ON FUTURE FILE FORMATS IN SCHEMA {dict['db']}.{schema} TO ROLE DR_RO;
GRANT USAGE ON ALL STAGES IN SCHEMA {dict['db']}.{schema} TO ROLE DR_RO;
GRANT USAGE ON FUTURE STAGES IN SCHEMA {dict['db']}.{schema} TO ROLE DR_RO;
GRANT SELECT ON ALL STREAMS IN SCHEMA {dict['db']}.{schema} TO ROLE DR_RO;
GRANT SELECT ON FUTURE STREAMS IN SCHEMA {dict['db']}.{schema} TO ROLE DR_RO;
GRANT OPERATE ON ALL TASKS IN SCHEMA {dict['db']}.{schema} TO ROLE DR_RO;
GRANT OPERATE ON FUTURE TASKS IN SCHEMA {dict['db']}.{schema} TO ROLE DR_RO;
GRANT SELECT ON ALL EXTERNAL TABLES IN SCHEMA {dict['db']}.{schema} TO ROLE DR_RO;
GRANT SELECT ON FUTURE EXTERNAL TABLES IN SCHEMA {dict['db']}.{schema} TO ROLE DR_RO;
'''
    return result



flag = str(sys.argv[1])

print(flag)
if(flag == 'Create'):
    print("Create flag")
else:
    print("Delete flag") 
dict = create_db_schema_dictionary()
dict['flag'] = 'Create' if flag == 'Create' else 'Delete'
opString1 = create_db_schema_roles(dict)
opString2 = ""
opString3 = create_warehouse(dict)
opString4 = ""
opString5 = ""
opString6 = ""


if dict['flag'] == 'Create':
    opString2 = create_role_privileges_mapping(dict)
    opString4 = create_warehouse_role_mapping(dict)
    opString5 = create_role_to_role_mapping(dict)
    opString6 = create_user_role_mapping(dict)
    
print(opString1)
print(opString2)
print(opString3)
print(opString4)
print(opString5)
print(opString6)

fop = opString1 + opString2 + opString3 + opString4 + opString5 + opString6

#createRole()
f = open("op.sql", "w")
f.write(fop)