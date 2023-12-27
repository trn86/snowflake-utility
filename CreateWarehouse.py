import yaml

def create_warehouse(dict):
    createWarehouseString = dict['SYSADMIN']
    commandStr = 'CREATE OR REPLACE WAREHOUSE ' if dict['flag'] == 'Create' else 'DROP WAREHOUSE '
    createWarehouseString = createWarehouseString + commandStr
    createWarehouseParams = ''' WITH WAREHOUSE_SIZE = "SMALL" AUTO_SUSPEND = 60 AUTO_RESUME = TRUE MIN_CLUSTER_COUNT = 1 MAX_CLUSTER_COUNT = 1 SCALING_POLICY = "ECONOMY"'''  if dict['flag'] == 'Create' else ''
    whString = ''
    with open('mapping.yaml', 'r') as file:
        configyml = yaml.safe_load(file)
        for wh in configyml['warehouses']:
          whString = whString + f''' {createWarehouseString}{wh}  {createWarehouseParams} ;\n'''
    #print(whString)
    return whString