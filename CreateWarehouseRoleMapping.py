import yaml

def create_warehouse_role_mapping(dict):
    whString = dict['SECURITYADMIN']
    with open('mapping.yaml', 'r') as file:
        configyml = yaml.safe_load(file)
        for wh in configyml['warehouses']:
          whString = whString + 'GRANT ALL PRIVILEGES ON WAREHOUSE ' + wh + " TO ROLE " + configyml['warehouseroles']['admin_role'] + ";\n" 
          whString = whString + 'GRANT USAGE ON WAREHOUSE ' + wh + " TO ROLE " + configyml['warehouseroles']['dev_role'] + ";\n"
    #print(whString)
    return whString

#createWarehouseRoleMapping()