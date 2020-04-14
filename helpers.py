import oci
import json
import pprint
from operator import itemgetter
from resource_info import get_resource_info_from_search
from oci_clients import clients_init
import asyncio
import time
import logging
import concurrent.futures as cf


def list_region_subscriptions(config):
    pprint.pprint("Fetching all regions in tenancy")
    identity_client = oci.identity.IdentityClient(config)
    tenancy_id = config['tenancy']
    regions = identity_client.list_region_subscriptions(tenancy_id=tenancy_id).data
    region_names = list(map(itemgetter("region_name"), oci.util.to_dict(regions)))
    pprint.pprint("List of regions subscribed to : {}".format(region_names))
    return region_names


def populate_search_results(region_name, search_client, resourceString, conditionString):
    search_client.base_client.set_region(region_name)
    search_details = oci.resource_search.models.StructuredSearchDetails(
        type="Structured",
        query="query " + resourceString + " resources where (" + conditionString + ")",
    )
    response = oci.pagination.list_call_get_all_results(
        search_client.search_resources, search_details=search_details
    )
    rawSearchData = json.dumps(convert_response_to_dict(response))
    with open("rawSearchData-" + region_name + ".json", "w") as f:
        f.write(rawSearchData)
    return True


def fetch_compartment_heirarchy(config):
    tenancy_id = config['tenancy']    
    pprint.pprint("Populate Compartment Herirachies in Tenancy")
    identity_client = oci.identity.IdentityClient(config)
    compartment_dict = fetch_all_compartments_in_tenancy(identity_client, tenancy_id)
    compartment_dict.append(
        convert_response_to_dict(identity_client.get_compartment(tenancy_id))
    )

    compartment_name_list = extract_value_by_field(compartment_dict, "name")
    compartment_ocid_list = extract_value_by_field(compartment_dict, "id")
    compartment_parentocid_list = extract_value_by_field(
        compartment_dict, "compartment_id"
    )

    compartment_kv = dict(zip(compartment_ocid_list, compartment_name_list))
    compartment_parent_ocid_kv = dict(
        zip(compartment_ocid_list, compartment_parentocid_list)
    )

    compartment_parentname_list = []
    for compartment_parent_ocid in compartment_parentocid_list:
        compartment_parentname_list.append(
            compartment_kv[compartment_parent_ocid]
            if compartment_parent_ocid in compartment_kv.keys()
            else "None"
        )
    return compartment_kv, compartment_parent_ocid_kv


def populate_SupportedShapeList(config, region_name, compute_client):
    shape_list = []
    tenancy_id = config['tenancy']
    compute_client.base_client.set_region(region_name)
    compute_shapes = convert_response_to_dict(compute_client.list_shapes(tenancy_id))
    shape_list.extend(list(compute_shape["shape"] for compute_shape in compute_shapes))

    shape_list = set(shape_list)
    OCPU_Count = list(
        shape_list_searchResult.split(".")[-1:][0]
        for shape_list_searchResult in shape_list
    )
    lookupTable = dict(zip(shape_list, OCPU_Count))
    lookupTable["VM.GPU.2.1"] = "1"
    lookupTable["VM.GPU2.1"] = "1"
    pprint.pprint("Populated Compute Shapes for region {}".format(region_name))
    return lookupTable

async def search_region_and_populate(
    executor,
    config,
    region_name,
    resourceString, 
    conditionString,
    compartment_kv,
    compartment_parent_ocid_kv):
    
    if region_name != "ap-hyderabad-1":
        tenancy_id = config['tenancy']
        # Set the region
        clients = await clients_init(config, region_name)
        computeShapeLookupTable = populate_SupportedShapeList(
            config, region_name, clients["Instance"]
        )
        region_distribution = []
        populate_search_results(region_name, clients["Search"], resourceString, conditionString)
        pprint.pprint(
            "Generated Raw Search Result JSON for region: {}".format(region_name)
        )

        with open("rawSearchData-" + region_name + ".json", "r") as f:
            rawSearchData = json.load(f)
        
        loop = asyncio.get_event_loop()
        region_distribution = [
            loop.run_in_executor(
                executor,
                get_resource_info_from_search,
                searchResult,
                tenancy_id,
                region_name,
                computeShapeLookupTable,
                clients,
                compartment_kv,
                compartment_parent_ocid_kv,
            )
            for searchResult in rawSearchData
        ]
        completed, pending = await asyncio.wait(region_distribution)
        completed_region = [t.result() for t in completed]
        region_distribution_json = json.dumps(completed_region)
        
        with open("region_distribution-" + region_name + ".json", "w") as f:
            f.write(region_distribution_json)

        pprint.pprint(
            "Generated Region Distribution JSON for region: {}".format(region_name)
        )
def convert_response_to_dict(oci_response):
    return oci.util.to_dict(oci_response.data)


def fetch_all_compartments_in_tenancy(client, tenancy_id):
    """Fetch all Compartments in Tenancy , and look across all subtrees."""
    compartmentResponse = oci.pagination.list_call_get_all_results(
        client.list_compartments,
        compartment_id=tenancy_id,
        limit=200,
        access_level="ACCESSIBLE",
        compartment_id_in_subtree=True,
        retry_strategy=oci.retry.DEFAULT_RETRY_STRATEGY,
    )
    return convert_response_to_dict(compartmentResponse)


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
