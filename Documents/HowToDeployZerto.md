# How To: Deploy Zerto For Kubernetes


Perform the following procedures:

1.	[Prepare Helm](#PrepareHelm)
2.	[Obtain the Image Pull Key Secret](#ObtaintheImagePullKeySecret)
3.	Next, select one of the following installation procedures:
  -	[Install Zerto for Kubernetes on a Kubernetes Cluster](#InstallZertoforKubernetesonaKubernetesCluster)
  - [Install Zerto Kubernetes Manager Proxy on Additional Kubernetes Clusters](#InstallZertoKubernetesManagerProxyonAdditionalKubernetesClusters)
  -	[Installing Zerto Kubernetes Manager on a Kubernetes Cluster](#InstallingZertoKubernetesManageronaKubernetesCluster)
4.	[Downloading the Zerto Operations Help Utility](#DownloadingtheZertoOperationsHelpUtility)

## Prepare Helm

On the Kubernetes platform, enter the following commands:

```
helm repo add zerto-z4k https://zapps-helm.zerto.com/z4k/stable
helm repo update
```

> Note:	Helm name (in the example above, zerto-z4k) should be a logical name entered by the user.

## Obtain the Image Pull Key Secret

1.	Go to [myZerto](https://www.zerto.com/myzerto/).
2.	If required, log in using your myZerto credentials.
3.	Navigate to [Support & Downloads > Software Downloads > Zerto for K8s](https://www.zerto.com/myzerto/support/downloads/#z4k), and click **Generate Registry Key**.
4.	Copy the Registry Key. You will need it later when installing the Zerto software.


## Install Zerto for Kubernetes on a Kubernetes Cluster

## Install Zerto Kubernetes Manager Proxy on Additional Kubernetes Clusters

## Installing Zerto Kubernetes Manager on a Kubernetes Cluster

## Downloading the Zerto Operations Help Utility
