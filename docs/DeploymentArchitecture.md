# Deploying Zerto for Kubernetes

Zerto helps customers accelerate IT transformation through a single, scalable platform for cloud data management and protection. 
Zerto for Kubernetes integrates continuous backup and disaster recovery into the application deployment lifecycle for containerized applications running on-premises or in the cloud as part of its cloud data management and protection platform. Easily protect and recover any Kubernetes application and its persistent data for accelerated delivery and deployment.
In a Kubernetes environment, Zerto for Kubernetes is installed and designed to protect next generation applications.

The installation includes the following:

-	**Zerto Kubernetes Manager (ZKM):** A containerized application that manages everything required for the replication between the protected and recovery clusters, apart from the actual replication of data. ZKM interacts with ZKM-PX as its proxy to a Kubernetes cluster and VRAs in order to orchestrate replication. ZKM manages the entire environment and therefore it is required to have only one instance of it.
-	**Zerto Kubernetes Manager Proxy (ZKM-PX):** A containerized application which serves as a communication proxy between the Kubernetes cluster and the VRA. Zerto requires one ZKM-PX installed per cluster.
-	**Virtual Replication Appliance (VRA):** A containerized application which is automatically installed on each cluster worker node. VRAs manage the replication of data from containers to the recovery cluster.
-	**Networking:** When replicating between clusters, Zerto requires ingress to manage all cross cluster communication. If replication is done within the same cluster, there is no need for this component.
-	**Keycloak:** Keycloak is an open source identity and access management tool which is used for user and component authentication. It is deployed automatically as part of the ZKM installation, and only one instance is required.
-	**Zerto Analytics:** A Zerto user interface which provides a view over all existing VPGs.

## Zerto for Kubernetes on a Single Kubernetes Cluster Deployment

[SingleCLuster](Images/Z4K_Single_Kubernetes_Cluster_Deployment.png?raw=true)

## Zerto for Kubernetes on Multiple Kubernetes Cluster Deployments

In this deployment Zerto recommends installing the Zerto Kubernetes Manager on the recovery cluster.

[MultipleCLuster](Images/Z4K_Multiple_Kubernetes_Cluster_Deployments.png?raw=true)

## Zerto for Kubernetes on Multiple Kubernetes Cluster Deployments - with a Separate Zerto Kubernetes Manager Cluster

In this deployment Zerto recommends installing the Zerto Kubernetes Manager on the recovery cluster.

[MultipleCLusterSeparateManager](Images/Z4K_Multiple_Kubernetes_Cluster_Deployments_Separate_ZKM.png?raw=true)
