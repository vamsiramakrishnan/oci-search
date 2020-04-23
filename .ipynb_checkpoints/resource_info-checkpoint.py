import oci
import json
from operator import itemgetter
from flatten_dict import flatten
from extract_info import get_resource_specific_info

def convert_response_to_dict(oci_response):
    return oci.util.to_dict(oci_response.data)

def extract_value_by_field(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    if v is not None:
                        arr.append(v)
                    else:
                        arr.append("None")
        elif isinstance(obj, list):
            for searchResult in obj:
                extract(searchResult, arr, key)
        elif isinstance(obj, type(None)):
            arr.append("None")

        return arr

    results = extract(obj, arr, key)
    return results


def get_resource_info_from_search(
    searchResult,
    tenancy_id,
    region_name,
    computeShapeLookupTable,
    clients,
    compartment_kv,
    compartment_parent_ocid_kv,
):
    parent_compartment_name = (
        compartment_kv[compartment_parent_ocid_kv[searchResult["compartment_id"]]]
        if searchResult["compartment_id"] != tenancy_id
        else "ROOT"
    )
    chosen_client = clients[searchResult["resource_type"]]
    try:
        searchResult, res_dict = get_resource_specific_info( 
            searchResult, computeShapeLookupTable, chosen_client
        )
    except:
        res_dict = {"resource_specific_info": "No Info"}
        pass
    
    norm_item_dict = {
        "region": region_name,
        "availability_domain": searchResult["availability_domain"],
        "resource_type": searchResult["resource_type"],
        "shape": searchResult["shape"],
        "OCPU_Qty": searchResult["OCPU_Qty"],
        "license_model": searchResult["license_model"],
        "display_name": searchResult["display_name"],
        "resource_ocid": searchResult["identifier"],
        "compartment_id": searchResult["compartment_id"],
        "compartment_name": compartment_kv[searchResult["compartment_id"]],
        "parent_compartment_name": parent_compartment_name,
        "CreatedBy": ("").join(extract_value_by_field(searchResult, "CreatedBy")),
        "CreatedOn": searchResult["time_created"]
    }
    norm_item_dict.update(res_dict)
    
    return norm_item_dict
