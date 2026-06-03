# CST8921 Lab 2： Cloud Security Trends

- Name: Bosi Chen
- Student ID: 041040774
- Course: CST8921 Cloud Industry Trends
- Lab: Lab 2
- Submission Date: Jun 3, 2026

## Introduction

This lab introduced key concepts of cloud security in Azure, focusing on controlling resource deployment, network segmentation, and data access restrictions. 

Cloud security ensures that only authorized users and systems can access cloud resources while blocking unauthorized or misconfigured access attempts.
In Azure, policies, virtual networks, network security groups, and storage firewalls work together to enforce secure cloud architecture and prevent unauthorized access to sensitive data.

## Tasks

### 1: Create Azure Policy – Allowed Locations

Created an Azure Policy to restrict resource deployment to Canada Central region only and validated that deployment outside Canada Central will fail.

![1-1](/Lab2/screenshots/1-1.png)
![1-2](/Lab2/screenshots/1-2.png)

### 2: Create a Virtual Network (Canada Central)

Created a virtual network in `Canada Central` region with address space `10.0.0.0/16`

![2](/Lab2/screenshots/2.png)

### 3: Create Subnets & Enable Storage Service Endpoint

Created two subnets with the following configurations:

| Subnet         | Address Range | Purpose         | Service Endpoint      |
| -------------- | ------------- | --------------- | --------------------- |
| private-subnet | 10.0.1.0/24   | Secure access   | Microsoft.Storage     |
| public-subnet  | 10.0.2.0/24   | Internet-facing | (no service endpoint) |


The service endpoint allows private subnet to access Azure Storage over Microsoft backbone network.

![3-1](/Lab2/screenshots/3-1.png)
![3-2](/Lab2/screenshots/3-2.png)
![3-3](/Lab2/screenshots/3-3.png)

### 4: Create Network Security Group (NSG)

Created a Network Security Group (NSG) and associated with `private-subnet` to control inbound and outbound network traffic.

The NSG was associated with the private subnet to enforce network-level security controls and restrict unauthorized traffic.

![4](/Lab2/screenshots/4.png)

### 5: Configure NSG Rules

Assign the following outbound rules to the NSG.

| Rule name            | Destination | Service Tag | Action | Priority |
| -------------------- | ----------- | ----------- | ------ | -------- |
| allow-azure-storage  | Service Tag | Storage     | Allow  | 100      |
| deny-internet-access | Service Tag | Internet    | Deny   | 200      |

This ensured that resources in the private subnet could not access the general Internet while still allowing access to Azure Storage services.

![5](/Lab2/screenshots/5.png)

### 6: Configure NSG for Public Subnet (RDP Access)

Added the following inbound rule:

| Rule name | Source | Port | Protocol |
| --------- | ------ | ---- | -------- |
| allow-rdp | Any    | 3389 | TCP      |

Public subnet allows remote administration via RDP.

![6](/Lab2/screenshots/6.png)

### 7: Create a Storage Account with File Share

Created a storage account with:

- Canada Central region
- Network access restricted to selected networks: only `private-subnet` allowed

Then created an Azure File Share inside the storage account.

Storage firewall will restrict access based on network rules.

![7-1](/Lab2/screenshots/7-1.png)
![7-2](/Lab2/screenshots/7-2.png)
![7-3](/Lab2/screenshots/7-3.png)

### 8: Deploy Virtual Machines

Deployed two VMs with the following configurations while same credentials were used for both virtual machines.

| VM Name    | Subnet         |
| ---------- | -------------- |
| vm-private | private-subnet |
| vm-public  | public-subnet  |

Azure Bastion was enabled for secure access.

![8-1-1](/Lab2/screenshots/8-1-1.png)
![8-1-2](/Lab2/screenshots/8-1-2.png)
![8-2-1](/Lab2/screenshots/8-2-1.png)
![8-2-2](/Lab2/screenshots/8-2-2.png)

### 9: Test Storage Access from Private Subnet (Allowed)

Connect to `vm-private` using Bastion.

Run the following PowerShell command to map Azure File Share to drive `Z:`:
```
$key = @{ 
    String = "<storage-account-key>" 
}
$acctKey = ConvertTo-SecureString @key -AsPlainText -Force

$cred = @{ 
    ArgumentList = "Azure\cst8921lab2storage", $acctKey 
}
$credential = New-Object System.Management.Automation.PSCredential @cred

$map = @{
    Name       = "Z"
    PSProvider = "FileSystem"
    Root       = "\\cst8921lab2storage.file.core.windows.net\file-share"
    Credential = $credential
}
New-PSDrive @map
```

Access was allowed because `vm-private` resides in an approved subnet with the storage access permissions.

![9](/Lab2/screenshots/9.png)

### 10: Test Storage Access from Public Subnet (Denied)

Connect to `vm-public` using Bastion.

Execute the PowerShell command above but got `Access is denied` as result.

Access was denied because `vm-public` was not included in the allowed network rules.

![10](/Lab2/screenshots/10.png)

### Cleanup

After completing the lab, all Azure resources were deleted.

## Validation Results Summary

| Scenario                                 | Expected Outcome | Actual Result |
| ---------------------------------------- | ---------------- | ------------- |
| Resource creation outside Canada Central | Blocked          | Blocked       |
| Storage access from private subnet       | Allowed          | Allowed       |
| Storage access from public subnet        | Denied           | Denied        |

## Security Analysis and Conclusion

This lab shows multiple layers of cloud security controls in Azure.
- Azure Policy was used to restrict resource deployment to an approved region. 
- Virtual Networks and subnet segmentation separated trusted and untrusted workloads.
- Network Security Groups provided traffic filtering by allowing Azure Storage access while blocking general internet access from the private subnet.
- The Storage Account was configured to allow access only from the private subnet, combined with the `Microsoft.Storage` Service Endpoint. This ensured that storage traffic remained on Azure’s backbone network and was inaccessible from unauthorized networks.

The successful access from `vm-private` and the denied access from `vm-public` validated that network-based access controls were functioning as required.