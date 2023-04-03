# Z4K Supported Platforms

Z4K can be deployed on multiple Kubernetes platforms.

The minimum supported Kubernetes version is 1.22.


| Platform                             | Version  |  CSI| Supported Kubernetes Versions |
| ------------------------------------ |--|--- |--- |
| Amazon Elastic Kubernetes Service (Amazon EKS)|  | ebs-csi-node | 1.22, 1.23  |
| Azure Kubernetes Service (AKS)|   |  csi-azuredisk-node   | 1.22, 1.23, 1.24  |
| Red Hat OpenShift | 4.6 and higher  |csi-rbdplugin  |  1.22  ||

<br/>
<br/>


Platforms previously tested or known to work can be viewed [here](./PreviouslyTestedPlatforms.md).


Zerto does not test and validate all Kubernetes distributions that can potentially be used by end users. 

It is the end users' responsibility to ensure that the distribution meets the following [prerequisites](https://help.zerto.com/bundle/Z4K-User-Documentation/page/PrerequisitesAndRequirements.html).

Zerto recommends that users perform functional tests like creating a VPG and performing a Failover prior to selecting any Kubernetes distribution.  
<br/>

If you need assistance for testing, please contact your Zerto account representative to engage with Zerto professional services.

If your specific distribution or CSI plugin is not listed above, please open a feature via the MyZerto portal. Requests will be evaluated but are not guaranteed within any specified period.
