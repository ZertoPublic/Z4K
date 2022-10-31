# Supported Platforms

Zerto for Kubernetes can be deployed on multiple Kubernetes platforms.

| Platform                             | Version  |  CSI| Notes |
| ------------------------------------ |--|--- |--- |
| Amazon Elastic Kubernetes Service (Amazon EKS)|  | ebs-csi-node | Supported up to version 1.22  |
| Azure Kubernetes Service (AKS)|   |  csi-azuredisk-node   |  |
| Red Hat OpenShift | 4.6 and higher  |csi-rbdplugin  |  ||

<span class="Note">Note: Z4K does not support XFS. </span>
