import json
from collections import OrderedDict
import netCDF4
import readNetCDF as rnc
import numpy as np

#File Locations
json_path = 'json_output_test.json'
nc_file = 'foam_2011-01-01.nc'

domain_type = "Grid" # Default

#Creating NetCDF dataset obkect
dset = rnc.load_netcdf(nc_file)

# ReadNetCDF data
rnc.extract_var_data(rnc.get_var_names(dset))
shape = rnc.get_shape(dset, 'ICEC')


def load_json(path):
    with open(path, 'r') as fp:
        return json.load(fp, object_pairs_hook=OrderedDict)

json_template = load_json(json_path)


def update_json(json_template, data, domain_type ):

    main_var = 'ICEC'
    json_template['domain']['domainType'] = domain_type
    # Coordinate data

    json_template['domain']['axes']['x']['values'] = data['lat'].tolist()
    json_template['domain']['axes']['y']['values'] = data['lon'].tolist()

    json_template['ranges'][main_var]['shape'] = rnc.get_shape(dset,main_var)
    json_template['ranges'][main_var]['values'] = (data[main_var].flatten().tolist())

    # Debug
    print(json.dumps(json_template,indent=4))

    json_template['domain']['axes']['z']['values'] = [5]


#ITest parameters
update_json(json_template,rnc.extract_var_data(rnc.get_var_names(dset)), "Grid")







