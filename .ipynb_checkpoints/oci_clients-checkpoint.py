import oci
import json
import pprint
import asyncio


async def clients_init(config, region_name):
    pprint.pprint("Initializing Resource Specific Clients & Regions ")
    
    #identity client
    pprint.pprint("Initialize Identity Client in Region : {}".format(region_name))
    identity_client = oci.identity.IdentityClient(config)
    identity_client.base_client.set_region(region_name)
    

    # search client
    pprint.pprint("Initialize Search Client in Region : {}".format(region_name))
    search_client = oci.resource_search.ResourceSearchClient(config)
    search_client.base_client.set_region(region_name)

    # Compute client
    pprint.pprint("Initialize Compute Client in Region : {}".format(region_name))
    compute_client = oci.core.ComputeClient(config)
    compute_client.base_client.set_region(region_name)

    # DB client
    pprint.pprint("Initialize DB Client in Region : {}".format(region_name))
    db_client = oci.database.DatabaseClient(config)
    db_client.base_client.set_region(region_name)

    # Analytics client
    pprint.pprint("Initialize Analytics Client in Region : {}".format(region_name))
    analytics_client = oci.analytics.AnalyticsClient(config)
    analytics_client.base_client.set_region(region_name)

    # VCN Client
    pprint.pprint("Initialize Networking Client in Region : {}".format(region_name))
    vcn_client = oci.core.VirtualNetworkClient(config)
    vcn_client.base_client.set_region(region_name)

    # Data Science
    pprint.pprint("Initialize Data Science Client in Region : {}".format(region_name))
    datascience_client = oci.data_science.DataScienceClient(config)
    datascience_client.base_client.set_region(region_name)

    # Block Storage
    pprint.pprint("Initialize Block Storage Client in Region : {}".format(region_name))
    blockstorage_client = oci.core.BlockstorageClient(config)
    blockstorage_client.base_client.set_region(region_name)

    # Object Storage
    pprint.pprint("Initialize Object Storage Client in Region : {}".format(region_name))
    objectstorage_client = oci.object_storage.ObjectStorageClient(config)
    objectstorage_client.base_client.set_region(region_name)

    # Notifications
    pprint.pprint("Initialize Notifications Client in Region : {}".format(region_name))
    notifications_client = oci.ons.NotificationControlPlaneClient(config)
    notifications_client.base_client.set_region(region_name)

    # APIGW
    pprint.pprint("Initialize API-GW Client in Region : {}".format(region_name))
    api_gw_client = oci.apigateway.GatewayClient(config)
    api_gw_client.base_client.set_region(region_name)
    api_gw_deployment_client = oci.apigateway.DeploymentClient(config)
    api_gw_deployment_client.base_client.set_region(region_name)

    # Streaming
    pprint.pprint("Initialize Streaming Client in Region : {}".format(region_name))
    streaming_client = oci.streaming.StreamAdminClient(config)
    streaming_client.base_client.set_region(region_name)

    # Functions
    pprint.pprint("Initialize Functions Client in Region : {}".format(region_name))
    functions_client = oci.functions.FunctionsManagementClient(config)
    functions_client.base_client.set_region(region_name)

    # Integration
    pprint.pprint("Initialize Integration Client in Region : {}".format(region_name))
    integration_client = oci.integration.IntegrationInstanceClient(config)
    integration_client.base_client.set_region(region_name)

    # Vaults
    pprint.pprint("Initialize Vaults Client in Region : {}".format(region_name))
    vaults_client = oci.vault.VaultsClient(config)
    vaults_client.base_client.set_region(region_name)

    # ODA
    pprint.pprint(
        "Initialize Oracle Digital Assistant Client in Region : {}".format(region_name)
    )
    oda_client = oci.oda.OdaClient(config)
    oda_client.base_client.set_region(region_name)

    # Datacatalog
    pprint.pprint("Initialize Data Catalog Client in Region : {}".format(region_name))
    datacatalog_client = oci.data_catalog.DataCatalogClient(config)
    datacatalog_client.base_client.set_region(region_name)

    # FileSystem
    pprint.pprint("Initialize File System Client in Region : {}".format(region_name))
    filestorage_client = oci.file_storage.FileStorageClient(config)
    filestorage_client.base_client.set_region(region_name)
    
    #Load Balancer
    pprint.pprint("Initialize Load balancer client in Region: {}".format(region_name))
    loadbalancer_client = oci.load_balancer.LoadBalancerClient(config)
    loadbalancer_client.base_client.set_region(region_name)

    return {
        "Vcn": vcn_client,
        "Subnet": vcn_client,
        "Instance": compute_client,
        "Image": compute_client,
        "AutonomousDatabase": db_client,
        "DbSystem": db_client,
        "AnalyticsInstance": analytics_client,
        "RouteTable": vcn_client,
        "SecurityList": vcn_client,
        "NatGateway": vcn_client,
        "ServiceGateway": vcn_client,
        "Vnic": vcn_client,
        "Search": search_client,
        "BootVolume": blockstorage_client,
        "Volume": blockstorage_client,
        "BootVolumeBackup": blockstorage_client,
        "VolumeBackup": blockstorage_client,
        "Stream": streaming_client,
        "Key": vaults_client,
        "Vault": vaults_client,
        "vaultSecret": vaults_client,
        "Bucket": objectstorage_client,
        "OdaInstance": oda_client,
        "VmCluster": db_client,
        "DataScienceProject": datascience_client,
        "DataScienceNotebookSession": datascience_client,
        "DataScienceModel": datascience_client,
        "DataCatalog": datacatalog_client,
        "OnsTopic": notifications_client,
        "ConnectHarness": streaming_client,
        "OnsSubscription": notifications_client,
        "ApiGateway": api_gw_client,
        "ApiDeployment": api_gw_deployment_client,
        "FileSystem": filestorage_client,
        "Compartment":identity_client,
        "Group": identity_client,
        "IdentityProvider": identity_client,
        "IdpGroupMapping": identity_client,
        "Policy": identity_client,
        "TagDefault": identity_client,
        "TagNamespace": identity_client,
        "User": identity_client,
        "FunctionsFunction": functions_client,
        "FunctionsApplication": functions_client,
        "LoadBalancer":loadbalancer_client,
        "LoadBalancerHealth":loadbalancer_client,
        "BackendSet":loadbalancer_client,
        "InternetGateway":vcn_client,
        "LocalPeeringGateway":vcn_client,
        "DynamicRoutingGateway":vcn_client,
        "PublicIp":vcn_client
        
    }
