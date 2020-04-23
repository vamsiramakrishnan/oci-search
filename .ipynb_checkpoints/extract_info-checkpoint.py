import oci
import json
from operator import itemgetter
from flatten_dict import flatten

def convert_response_to_dict(oci_response):
    response_dict =  oci.util.to_dict(oci_response.data)
    return response_dict

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
    vnic_dict = convert_response_to_dict(compute_client.list_vnic_attachments(compartment_id = searchResult['compartment_id'], availability_domain = searchResult['availability_domain'], instance_id = searchResult["identifier"]))
    volume_dict = convert_response_to_dict(compute_client.list_volume_attachments(compartment_id = searchResult['compartment_id'], availability_domain = searchResult['availability_domain'], instance_id = searchResult["identifier"]))
    boot_volume_dict = convert_response_to_dict(compute_client.list_boot_volume_attachments(compartment_id = searchResult['compartment_id'], availability_domain = searchResult['availability_domain'], instance_id = searchResult["identifier"]))
    compute_dict.update({"vnic_attachments": vnic_dict})
    compute_dict.update({"volume_attachments": volume_dict})
    compute_dict.update({"boot_volume_attachments": boot_volume_dict})
    searchResult["shape"] = compute_dict["shape"]
    searchResult["OCPU_Qty"] = computeShapeLookupTable[compute_dict["shape"]]
    return searchResult, compute_dict

def extract_image(searchResult, computeShapeLookupTable, compute_client):
    image_dict = convert_response_to_dict(
        compute_client.get_image(searchResult["identifier"])
    )
    return image_dict

def extract_analytics(searchResult, computeShapeLookupTable, analytics_client):
    analytics_dict = convert_response_to_dict(
        analytics_client.get_analytics_instance(searchResult["identifier"])
    )
    searchResult["OCPU_Qty"] = analytics_dict["capacity"]["capacity_value"]
    searchResult["license_model"] = analytics_dict["license_type"]
    return searchResult, analytics_dict


def extract_vcn(searchResult, computeShapeLookupTable, vcn_client):
    vcn_dict = convert_response_to_dict(vcn_client.get_vcn(searchResult["identifier"]))
    igw_dict =  convert_response_to_dict(vcn_client.list_internet_gatways(compartment_id = searchResult['compartment_id'], vcn_id = searchResult['identifier']))
    lpg_dict =  convert_response_to_dict(vcn_client.list_local_peering_gatways(compartment_id = searchResult['compartment_id'], vcn_id = searchResult['identifier']))
    
    vcn_dict.update({"internet_gateways": igw_dict})
    vcn_dict.update({"local_peering_gateways": lpg_dict})
    
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

def extract_user(searchResult, computeShapeLookupTable, identity_client):
    user_dict = convert_response_to_dict(
        identity_client.get_user(searchResult["identifier"]))
    memberships_dict =  convert_response_to_dict(identity_client.list_user_group_memberships(searchResult['compartment_id'], user_id = searchResult["identifier"]))
    user_dict.update({"group_memberships": memberships_dict})
    return user_dict

def extract_compartment(searchResult, computeShapeLookupTable, identity_client):
    compartment_dict = convert_response_to_dict(
        identity_client.get_compartment(searchResult["identifier"])
    )
    return compartment_dict

def extract_group(searchResult, computeShapeLookupTable, identity_client):
    group_dict = convert_response_to_dict(
        identity_client.get_group(searchResult["identifier"])
    )
    return group_dict

def extract_tagdefault(searchResult, computeShapeLookupTable, identity_client):
    td_dict = convert_response_to_dict(
        identity_client.get_tag_default(searchResult["identifier"])
    )
    return td_dict

def extract_policy(searchResult, computeShapeLookupTable, identity_client):
    policy_dict = convert_response_to_dict(
        identity_client.get_policy(searchResult["identifier"])
    )
    return policy_dict


def extract_tagnamespace(searchResult, computeShapeLookupTable, identity_client):
    tagnamespace_dict = convert_response_to_dict(
        identity_client.get_tag_namespace(searchResult["identifier"])
    )
    return tagnamespace_dict

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

def extract_datascience_project(searchResult, computeShapeLookupTable, datascience_client):
    datascience_dict = convert_response_to_dict(
        datascience_client.get_project(searchResult["identifier"])
    )
    return datascience_dict

def extract_datascience_notebook_session(searchResult, computeShapeLookupTable, datascience_client):
    datascience_dict = convert_response_to_dict(
        datascience_client.get_notebook_session(searchResult["identifier"])
    )
    return datascience_dict

def extract_datascience_model(searchResult, computeShapeLookupTable, datascience_client):
    datascience_dict = convert_response_to_dict(
        datascience_client.get_model(searchResult["identifier"])
    )
    return datascience_dict

def extract_fnapplication(searchResult, computeShapeLookupTable, fnapplication_dict):
    fnapplication_dict = convert_response_to_dict(
        fnapplication_dict.get_application(searchResult["identifier"])
    )
    return fnapplication_dict

def extract_fn(searchResult, computeShapeLookupTable, fnapplication_dict):
    fn_dict = convert_response_to_dict(
        fnapplication_dict.get_function(searchResult["identifier"])
    )
    return fn_dict
    

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

    elif searchResult["resource_type"] == "VolumeBackup":
        res_dict = extract_volume_backup(searchResult, computeShapeLookupTable, client)
        
    elif searchResult["resource_type"] == "FileStorage":
        res_dict = extract_filestorage(searchResult, computeShapeLookupTable, client)
        
    elif searchResult["resource_type"] == "Compartment":
        res_dict = extract_compartment(searchResult, computeShapeLookupTable, client)
    
    elif searchResult["resource_type"] == "User":
        res_dict = extract_user(searchResult, computeShapeLookupTable, client)

    elif searchResult["resource_type"] == "Group":
        res_dict = extract_group(searchResult, computeShapeLookupTable, client)

    elif searchResult["resource_type"] == "TagNamespace":
        res_dict = extract_tagnamespace(searchResult, computeShapeLookupTable, client)

    elif searchResult["resource_type"] == "TagDefault":
        res_dict = extract_tagdefault(searchResult, computeShapeLookupTable, client)

    elif searchResult["resource_type"] == "Policy":
        res_dict = extract_policy(searchResult, computeShapeLookupTable, client)
        
    elif searchResult["resource_type"] == "DataScienceProject":
        res_dict = extract_datascience_project(searchResult, computeShapeLookupTable, client)

    elif searchResult["resource_type"] == "DataScienceNotebookSession":
        res_dict = extract_datascience_notebook_session(searchResult, computeShapeLookupTable, client)

    elif searchResult["resource_type"]== "DataScienceModel":
        res_dict = extract_datascience_model(searchResult, computeShapeLookupTable, client)
        
    elif searchResult["resource_type"]=="Image":
        res_dict = extract_image(searchResult, computeShapeLookupTable, client)
        
    elif searchResult["resource_type"]=="FunctionsApplication":
        res_dict =  extract_fnapplication(searchResult, computeShapeLookupTable, client)
        
    elif searchResult["resource_type"]=="FunctionsFunction":
        res_dict =  extract_fn(searchResult, computeShapeLookupTable, client)        
        
    return searchResult, res_dict
