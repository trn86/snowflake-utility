import yaml

def create_user_role_mapping(dict):
    userRoleGrantString = dict['SECURITYADMIN']
    with open('mapping.yaml', 'r') as file:
        configyml = yaml.safe_load(file)
        for user in configyml['admin_user']:
            userRoleGrantString = userRoleGrantString + 'GRANT ROLE ' + configyml['functionalroles']['admin_role'] + " TO USER " + user + ";\n" 
        for user in configyml['developer_user']:
            userRoleGrantString = userRoleGrantString + 'GRANT ROLE ' + configyml['functionalroles']['dev_role'] + " TO USER " + user + ";\n" 
        for user in configyml['analyst_user']:
            userRoleGrantString = userRoleGrantString + 'GRANT ROLE ' + configyml['functionalroles']['analyst_role'] + " TO USER " + user + ";\n"
    #print(userRoleGrantString)
    return userRoleGrantString

#createUserRoleMapping()