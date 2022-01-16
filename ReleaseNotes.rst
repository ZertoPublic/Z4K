Zerto helps customers accelerate IT transformation through a single, scalable platform for cloud data management and protection. Built for enterprise scale, Zerto’s simple, software-only platform uses continuous data protection to converge disaster recovery, backup, and data mobility and eliminate the risks and complexity of modernization and cloud adoption. Zerto enables an always-on customer experience by simplifying the protection, recovery, and mobility of applications and data across private, public, and hybrid clouds. Zerto is trusted by over 9,500 customers globally and is powering offerings for Microsoft Azure, IBM Cloud, AWS, Google Cloud, Oracle Cloud, and more than 450 managed service providers.

Zerto for Kubernetes integrates continuous backup and disaster recovery into the application deployment lifecycle for containerized applications running on-premises or in the cloud as part of its cloud data management and protection platform. Easily protect and recover any Kubernetes application and its persistent data for accelerated delivery and deployment. Introducing:

•	Data protection as code: Purpose-built for Kubernetes, Zerto integrates both backup and disaster recovery into the application deployment lifecycle from day one while enabling rapid development.
•	Continuous data protection: Always-on replication provides continuous protection for automated, non-disruptive recovery of containerized applications within and between clusters, datacenters, or clouds. Zerto pioneers a continuous approach to protecting Kubernetes applications that doesn’t rely on legacy approaches such as snapshots. Zerto delivers the performance and simplicity required to successfully protect and recover containerized applications.
•	Easily managed via API: Zerto is managed via API, allowing easy integration into existing automation tools used in Kubernetes clusters. Simplifying operations and protection for developers and DevOps engineers.
•	Hybrid and multi-cloud: Native support for your Kubernetes environments, no matter where they’re running: on-premises or in the cloud, use Zerto to protect to, from, and between the platform of your choice.
•	Environment and application awareness: Protect and recover complex applications as one consistent entity.
•	Complete visibility and monitoring: Zerto delivers a centralized view of your entire Kubernetes environment to monitor performance and protection.
•	Simple, native workflows: Simple, built-in workflows for any recovery and orchestration scenario designed to streamline operations.
The following topics are described in these Release Notes:

•	Supported Kubernetes Platforms
•	Deploying Zerto for Kubernetes
•	Zerto for Kubernetes - Known Issues
Supported Kubernetes Platforms
Zerto for Kubernetes can be deployed on multiple Kubernetes platforms:
•	Amazon Elastic Kubernetes Service (Amazon EKS)
•	Azure Kubernetes Service (AKS)
•	Google Kubernetes Engine (GKE)
•	Red Hat OpenShift
•	IBM Cloud Kubernetes Service (IKS)
Deploying Zerto for Kubernetes
In a Kubernetes environment, Zerto for Kubernetes is installed and designed to protect next generation applications.

The installation includes the following:

•	Zerto Kubernetes Manager (ZKM): A containerized application that manages everything required for the replication between the protected and recovery clusters, apart from the actual replication of data. ZKM interacts with ZKM-PX as its proxy to a Kubernetes cluster and VRAs in order to orchestrate replication. ZKM manages the entire environment and therefore it is required to have only one instance of it.
•	Zerto Kubernetes Manager Proxy (ZKM-PX): A containerized application which serves as a communication proxy between the Kubernetes cluster and the VRA. Zerto requires one ZKM-PX installed per cluster.
•	Virtual Replication Appliance (VRA): A containerized application which is automatically installed on each cluster node. VRAs manage the replication of data from containers to the recovery cluster.
•	Networking: When replicating between clusters, Zerto requires ingress to manage all cross cluster communication. If replication is done within the same cluster, there is no need for this component.
•	Keycloak: Keycloak is an open source identity and access management tool which is used for user and component authentication. It is deployed automatically as part of the ZKM installation, and only one instance is required.
•	Zerto Analytics: A Zerto user interface which provides a view over all existing VPGs.
For deployment prerequisites, installation instructions, and initial use, click here.

Zerto for Kubernetes - Known Issues
Red Hat OpenShift

•	Zerto for Kubernetes only supports from OpenShift version 4.6 or higher.
Google Kubernetes Engine (GKE)

•	COS nodes are not supported. And therefore, Autopilot deployment is not supported.
VMware Tanzu

•	VMware Tanzu Kubernetes Grid (TKG) will be supported by Zerto for Kubernetes at a later date, pending compliance from VMware.
Oracle Container Engine

•	Oracle Container Engine for Kubernetes (OKE) will be supported by Zerto for Kubernetes at a later date, pending compliance from Oracle.
