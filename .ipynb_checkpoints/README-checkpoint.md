# SEARCH & GRAPH
This repo is a project to enhance tenancy visibility with the help of OCI Search + OCI Python SDK + AsyncIO Python+ Concurrent Futures + NetworkX + Pandas + Oracle Data Visualization  + Cytoscape.


# ARCHITECTURE
## DATA FETCH LAYER
1. *OCI Search* - Fast return of resources OCIDs  OCI Search is an Indes
2. *OCI Python SDK GET & LIST* Detailed Information on every resource
3. *ASYNCIO PYTHON*- Non-Blocking Requests & Responses 
4. *CONCURRENT FUTURE* - Asynchronous Parallelism for fetch
5. *NETWORKX*- Graph Library with familiar Dict & List Data Structures
6. *PANDAS* - Relational Library with familiar Dict & List Data Structures
7. *ORACLE DATA VIZ DESKTOP* - Desktop Data Visualization to generate Canvas & Dashboards
8. *CYTOSCAPE* - GraphViz tool for interacting with Graphs

# Link to Notebook: 
[Search & Graph ](https://github.com/vamsiramakrishnan/oci-search/blob/master/fetch-imp-resources.ipynb)

# Suggested reading 
1. [Parallel Async Python + OCI Search ](https://medium.com/@vamsiramakrishnan/accelerate-tenancy-visibility-with-oracle-cloud-infrastructure-search-asyncio-parallel-python-4bc31d543ec)
2. [Graphing OCI Infrastructure](https://medium.com/@vamsiramakrishnan/apply-graph-theory-to-oracle-cloud-infrastructure-with-python-networkx-cytoscape-f07f72951b53)

## Resources Supported

### **Compute**
    instances
    image

### **Block, Object & File Storage**
    bootvolume
    bootvolumebackup
    volumebackup
    volumebackuppolicy
    volume
    bucket
    filesystem

### **DataScience, Integration & AI**
    datascienceproject
    datasciencemodel
    datasciencenotebooksession
    datacatalog
    odainstance
    integrationinstance

### **Database & Analytics**
    analyticsinstance
    autonomousdatabase
    dbsystem
    vmcluster

### **Networking**
    vcn
    subnet
    vnic
    securitylist
    routetable
    natgateway
    servicegateway

### **Cloud Native**
    onstopic
    onssubscription
    stream
    connectharness
    apigateway
    apideployment

### **Key Management**
    vault

### **IAM**
    compartment
    group
    identityprovider
    idpgroupmapping
    policy
    tagdefault
    tagnamespace
    user


# What does the notebook do
- Generates a Raw Search Output File  One per region
- Generates a Processed JSON File with Additional Resource Metadata One Per Region
- A Consolidated CSV and JSON file with consolidated information across regions.
- Consolidated GraphML File for all regions suitable for load in Cytoscape

# Pre-Requisites
* Setup OCI-CLI
* Run with Tenancy Administrator Privileges
* Python Version 3.6+
* OCI Library installed via PIP
* Other Modules - Refer Requirements.txt
