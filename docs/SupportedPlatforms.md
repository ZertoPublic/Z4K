# Supported Platforms

| Platform                             | Version  |  CSI| Notes |
| ------------------------------------ |--|--- |--- |
| Amazon Elastic Kubernetes Service (Amazon EKS)|  | ebs-csi-node | Supported up to version 1.22  |
| Azure Kubernetes Service (AKS)|   |  csi-azuredisk-node   |  |
| Red Hat OpenShift | 4.6 and higher  |csi-rbdplugin  |  ||

Zerto does not test and validate all Kubernetes distributions that can potentially be used by end users. It is the end users' responsibility to ensure that the distribution meets the prerequisites.

Zerto recommends that users perform functional tests like creating a VPG and performing a Failover prior to selecting any Kubernetes distribution.  

If you need assistance for testing, contact your Zerto account representative to engage with Zerto professional services.

<span class="Note">Kubernetes distribution incompatibility or performance issues cannot be addressed by opening support tickets with Zerto. Instead, an idea request via the MyZerto portal should be created. Requests will be evaluated, but are not a guaranteed within any specified period.</span>
