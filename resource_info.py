import oci
import json
from operator import itemgetter


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

def extract_db(searchResult, computeShapeLookupTable, db_client):
    db_dict = convert_response_to_dict(
        db_client.get_db_system(searchResult["identifier"])
    )
    searchResult["shape"] = db_dict["shape"]
    searchResult["OCPU_Qty"] = computeShapeLookupTable[db_dict["shape"]]
    searchResult["license_model"] = db_dict["license_model"]
    return searchResult, db_dict


def extract_autonomousDb(searchResult, computeShapeLookupTable, db_client):
    adb_dict = convert_response_to_dict(
        db_client.get_autonomous_database(searchResult["identifier"])
    )
    searchResult["license_model"] = adb_dict["license_model"]
    searchResult["OCPU_Qty"] = adb_dict["cpu_core_count"]
    return searchResult, adb_dict


def extract_compute(searchResult, computeShapeLookupTable, compute_client):
    compute_dict = convert_response_to_dict(
        compute_client.get_instance(searchResult["identifier"])
    )
    searchResult["shape"] = compute_dict["shape"]
    searchResult["OCPU_Qty"] = computeShapeLookupTable[compute_dict["shape"]]
    return searchResult, compute_dict


def extract_analytics(searchResult, computeShapeLookupTable, analytics_client):
    analytics_dict = convert_response_to_dict(
        analytics_client.get_analytics_instance(searchResult["identifier"])
    )
    searchResult["OCPU_Qty"] = analytics_dict["capacity"]["capacity_value"]
    searchResult["license_model"] = analytics_dict["license_type"]
    return searchResult, analytics_dict


def extract_vcn(searchResult, computeShapeLookupTable, vcn_client):
    vcn_dict = convert_response_to_dict(vcn_client.get_vcn(searchResult["identifier"]))
    return vcn_dict


def extract_subnet(searchResult, computeShapeLookupTable, vcn_client):
    subnet_dict = convert_response_to_dict(
        vcn_client.get_subnet(searchResult["identifier"])
    )
    return subnet_dict


def extract_natgateway(searchResult, computeShapeLookupTable, vcn_client):
    natgw_dict = convert_response_to_dict(
        vcn_client.get_nat_gateway(searchResult["identifier"])
    )
    return natgw_dict


def extract_servicegateway(searchResult, computeShapeLookupTable, vcn_client):
    sgw_dict = convert_response_to_dict(
        vcn_client.get_service_gateway(searchResult["identifier"])
    )
    return sgw_dict


def extract_securitylist(searchResult, computeShapeLookupTable, vcn_client):
    sl_dict = convert_response_to_dict(
        vcn_client.get_security_list(searchResult["identifier"])
    )
    return sl_dict


def extract_vnic(searchResult, computeShapeLookupTable, vcn_client):
    vnic_dict = convert_response_to_dict(
        vcn_client.get_vnic(searchResult["identifier"])
    )
    return vnic_dict


def extract_routetable(searchResult, computeShapeLookupTable, vcn_client):
    rt_dict = convert_response_to_dict(
        vcn_client.get_route_table(searchResult["identifier"])
    )
    return rt_dict

def extract_routetable(searchResult, computeShapeLookupTable, vcn_client):
    rt_dict = convert_response_to_dict(
        vcn_client.get_route_table(searchResult["identifier"])
    )
    return rt_dict


def extract_bucket(searchResult, computeShapeLookupTable, objectstorage_client):
    namespace = convert_response_to_dict(objectstorage_client.get_namespace())
    fields = ["approximateCount"]
    bucket_dict = convert_response_to_dict(
        objectstorage_client.get_bucket(
        namespace_name =  namespace, 
        bucket_name = searchResult["display_name"], fields = fields)
    )
    return bucket_dict

def extract_volume(searchResult, computeShapeLookupTable, blockstorage_client):
    volume_dict = convert_response_to_dict(
        blockstorage_client.get_volume(searchResult["identifier"])
    )
    return volume_dict

def extract_bootvolume(searchResult, computeShapeLookupTable, blockstorage_client):
    bootvolume_dict = convert_response_to_dict(
        blockstorage_client.get_boot_volume(searchResult["identifier"])
    )
    return bootvolume_dict

def extract_bootvolume_backup(searchResult, computeShapeLookupTable, blockstorage_client):
    bootvolume_backup_dict = convert_response_to_dict(
        blockstorage_client.get_boot_volume_backup(searchResult["identifier"])
    )
    return bootvolume_backup_dict


def extract_volume_backup(searchResult, computeShapeLookupTable, blockstorage_client):
    volume_backup_dict = convert_response_to_dict(
        blockstorage_client.get_volume_backup(searchResult["identifier"])
    )
    return volume_backup_dict

def extract_filestorage(searchResult, computeShapeLookupTable, filestorage_client):
    filestorage_dict = convert_response_to_dict(
        filestorage_client.get_file_system(searchResult["identifier"])
    )
    return filestorage_dict

def get_resource_specific_info( searchResult, computeShapeLookupTable, client):
    searchResult["license_model"] = "N/A"
    searchResult["shape"] = "N/A"
    searchResult["OCPU_Qty"] = "N/A"
    res_dict = {"searchResultSpecificInfo": "N/A"}

    if searchResult["resource_type"] == "DbSystem":
        searchResult, res_dict = extract_db(
            searchResult, computeShapeLookupTable, client
        )
    elif searchResult["resource_type"] == "Instance":
        searchResult, res_dict = extract_compute(
            searchResult, computeShapeLookupTable, client
        )
    elif searchResult["resource_type"] == "AnalyticsInstance":
        searchResult, res_dict = extract_analytics(
            searchResult, computeShapeLookupTable, client
        )
    elif searchResult["resource_type"] == "AutonomousDatabase":
        searchResult, res_dict = extract_autonomousDb(
            searchResult, computeShapeLookupTable, client
        )
    elif searchResult["resource_type"] == "Vcn":
        res_dict = extract_vcn(searchResult, computeShapeLookupTable, client)
        
    elif searchResult["resource_type"] == "Subnet":
        res_dict = extract_subnet(searchResult, computeShapeLookupTable, client)
        
    elif searchResult["resource_type"] == "RouteTable":
        res_dict = extract_routetable(searchResult, computeShapeLookupTable, client)
        
    elif searchResult["resource_type"] == "SecurityList":
        res_dict = extract_securitylist(searchResult, computeShapeLookupTable, client)
        
    elif searchResult["resource_type"] == "ServiceGateway":
        res_dict = extract_servicegateway(searchResult, computeShapeLookupTable, client)
        
    elif searchResult["resource_type"] == "NatGateway":
        res_dict = extract_natgateway(searchResult, computeShapeLookupTable, client)
        
    elif searchResult["resource_type"] == "Vnic":
        res_dict = extract_vnic(searchResult, computeShapeLookupTable, client)
        
    elif searchResult["resource_type"] == "Bucket":
        res_dict = extract_bucket(searchResult, computeShapeLookupTable, client)
        
    elif searchResult["resource_type"] == "BootVolume":
        res_dict = extract_bootvolume(searchResult, computeShapeLookupTable, client)
        
    elif searchResult["resource_type"] == "Volume":
        res_dict = extract_volume(searchResult, computeShapeLookupTable, client)
        
    elif searchResult["resource_type"] == "BootVolumeBackup":
        res_dict = extract_bootvolume_backup(searchResult, computeShapeLookupTable, client)
        
    elif searchResult["resource_type"] == "FileStorage":
        res_dict = extract_filestorage(searchResult, computeShapeLookupTable, client)
        
    elif searchResult["resource_type"] == "VolumeBackup":
        res_dict = extract_volume_backup(searchResult, computeShapeLookupTable, client)
    
    return searchResult, res_dict



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
        else "None"
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