## Platforms Previously Tested or Known to Work with Zerto for Kubernetes
</br>
</br>

| Platform                             | Version  |  CSI| Notes |
| ------------------------------------ |--|--- |--- |
| Google Kubernetes Engine (GKE)|   | pdcsi-node | COS nodes are not supported. Therefore, Autopilot deployment is not supported.|  |
| HPE Ezmeral | 5.3 & 5.4 |csi-nodeplugin-kdf, pdcsi-node|  |
| IBM Cloud Kubernetes Service (IKS) |  | ibm-vpc-block-csi-node |   |
| Oracle Container Engine for Kubernetes (OKE) |   |csi-oci-node |Supported in combination with Rook. |
| VMware Tanzu  | VMware 6.7 | vsphere-csi-node |Supported in combination with Rook. |
|   | VMware 7.0u2 |vsphere-csi-node |Full native support. <br> Kubernetes 1.19.9\1.20.5 or higher (CSI Block device support) on top of Tanzu Kubernetes Grid (TKG) is supported.  ||
