import json

def cf_params_to_keys(collection):
    """
        Given a collection that looks like:

        "[
            {
                "ParameterKey": "InstanceType",
                "ParameterValue": "t2.medium"
            }
         ]
        "

        We need to transform it into a Python dictionary that looks like

        {"InstanceType": "t2.medium"}

        @param collection an instance of AnsibleUnsafeText
    """

    # print(type(collection).name)
    res = json.loads(collection)
    output = {}
    for current in res:
        output[ current.get("ParameterKey") ] = current.get("ParameterValue")
    
    return output


class FilterModule(object):
    def filters(self):
        return {'cf_params_to_keys': cf_params_to_keys}