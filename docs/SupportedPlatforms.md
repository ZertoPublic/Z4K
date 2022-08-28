# Supported Platforms

Zerto for Kubernetes can be deployed on multiple Kubernetes platforms.

| Platform                             | Version |CSI|Notes |
| ------------------------------------ |--|--|------ |
| Amazon Elastic Kubernetes Service (Amazon EKS)|  | ebs-csi-node |  |
| Azure Kubernetes Service (AKS)|   | csi-azuredisk-node   |  |
| Google Kubernetes Engine (GKE)|  | pdcsi-node | COS nodes are not supported. Therefore, Autopilot deployment is not supported.|  |
| Red Hat OpenShift | 4.6 and higher  | |  |  |
| IBM Cloud Kubernetes Service (IKS) |  |  |  |
| Oracle Container Engine for Kubernetes (OKE) |  |csi-oci-node  |Supported in combination with Rook. |
| VMware Tanzu  | VMware 6.7 | vsphere-csi-node |Supported in combination with Rook. |
|   | VMware 7.0u2 | vsphere-csi-node |Full native support. <br> Kubernetes 1.19.9\1.20.5 or higher (CSI Block device support) on top of Tanzu Kubernetes Grid (TKG) is supported.  ||
| HPE |  | csi-nodeplugin-kdf           <br> pdcsi-node|  |  |

