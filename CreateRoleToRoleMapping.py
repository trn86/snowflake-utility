import yaml

def create_role_to_role_mapping(dict):
    roleGrantString = dict['SECURITYADMIN']
    with open('mapping.yaml', 'r') as file:
        configyml = yaml.safe_load(file)
        roleGrantString = roleGrantString + 'GRANT ROLE ' + configyml['databaseroles']['admin_role'] + " TO ROLE " + configyml['functionalroles']['admin_role'] + ";\n" 
        roleGrantString = roleGrantString + 'GRANT ROLE ' + configyml['databaseroles']['dev_role'] + " TO ROLE " + configyml['functionalroles']['dev_role'] + ";\n" 
        roleGrantString = roleGrantString + 'GRANT ROLE ' + configyml['databaseroles']['analyst_role'] + " TO ROLE " + configyml['functionalroles']['analyst_role'] + ";\n"

        roleGrantString = roleGrantString + 'GRANT ROLE ' + configyml['serviceintegrationroles'][0] + " TO ROLE " + configyml['functionalroles']['admin_role'] + ";\n" 
        roleGrantString = roleGrantString + 'GRANT ROLE ' + configyml['serviceintegrationroles'][0] + " TO ROLE " + configyml['functionalroles']['analyst_role'] + ";\n" 

        roleGrantString = roleGrantString + 'GRANT ROLE ' + configyml['functionalroles']['analyst_role'] + " TO ROLE " + configyml['functionalroles']['dev_role'] + ";\n" 
        roleGrantString = roleGrantString + 'GRANT ROLE ' + configyml['functionalroles']['dev_role'] + " TO ROLE " + configyml['functionalroles']['admin_role'] + ";\n" 
        roleGrantString = roleGrantString + 'GRANT ROLE ' + configyml['functionalroles']['admin_role'] + " TO ROLE " + configyml['parent_snowflake_role'] + ";\n"

        roleGrantString = roleGrantString + 'GRANT ROLE ' + configyml['serviceintegrationroles'][0] + " TO ROLE " + configyml['functionalroles']['dev_role'] + ";\n" 
        roleGrantString = roleGrantString + 'GRANT ROLE ' + configyml['serviceintegrationroles'][0] + " TO ROLE " + configyml['functionalroles']['admin_role'] + ";\n" 

        roleGrantString = roleGrantString + 'GRANT ROLE ' + configyml['warehouseroles']['admin_role'] + " TO ROLE " + configyml['functionalroles']['admin_role'] + ";\n" 
        roleGrantString = roleGrantString + 'GRANT ROLE ' + configyml['warehouseroles']['dev_role'] + " TO ROLE " + configyml['functionalroles']['dev_role'] + ";\n"
    #print(roleGrantString)
    return roleGrantString

#dict = {'SECURITYADMIN' : 'abc'}
#print(createRoleToRoleMapping(dict))