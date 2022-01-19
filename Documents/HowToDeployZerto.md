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

![PullKey](Images/PullKey.png?raw=true)

## Install Zerto for Kubernetes on a Kubernetes Cluster

This installation includes the following:

-	Zerto Kubernetes Manager (ZKM)
-	Zerto Kubernetes Manager Proxy (ZKM-PX)

The following are commands to install Zerto for Kubernetes on any one of the Zerto supported Kubernetes platforms.

Perform one of the following:

1.	Either enter the following commands:

```
helm install <installation names> zerto-z4k/z4k \
--set global.imagePullSecret=$IMAGE_PULL_KEY \
--set global.authentication. managementUser=$KEYCLOAK_USER
--set global.authentication. managementPassword =$KEYCLOAK_PASSWORD
--set global.authentication. adminUser =$ADMIN_USER
--set global.authentication. adminPassword =$ADMIN_PASSWORD
--set zkm-px.config.siteId=$SITE \
--namespace $NAMESPACE
```

2.	Or, first create the following values.yaml:

```
global:
authentication:
adminPassword: $ADMIN_PASSWORD
adminUser: $ADMIN_USER
managementPassword: $KEYCLOAK_PASSWORD
managementUser: $KEYCLOAK_USER
imagePullSecret: $IMAGE_PULL_KEY
zkm-px:

config:
siteId: $SITE
```

And then install using the following command:

```
helm install <installation names> zerto-z4k/z4k -f values.yaml --namespace $NAMESPACE
```

In **OpenShift on VMware platforms**, Zerto does not deploy its own ingress controller but rather utilizes the built-in routes.
As such, to enable VRA communication, you need to disable ingress deployment and provide the external IP of the sites.

-	To do this, enter the following commands:

```
--set zkm.zkmIngressControllerEnabled =false
--set zkm-px.zkmProxyIngressControllerEnabled =false
--set zkm-px.config.externalIp=$SITE_IP
--set zkm.useNginxRoutePath=false
```

Consider the following:

| Parameter | Comment |
| --------- | ------- |
| installation names | Specify an easy to recognize name. |
| $NAMESPACE | A dedicated Zerto namespace. We recommend using the namespace zerto. |
| $SITE |	A unique site name. |

## Install Zerto Kubernetes Manager Proxy on Additional Kubernetes Clusters

This installation includes the following:

-	Zerto Kubernetes Manager Proxy (ZKM-PX)
1.	[Get an initial access token from Keycloak](#)
2.	[Install Zerto Kubernetes Manager Proxy on Additional Clusters](#)

## Installing Zerto Kubernetes Manager on a Kubernetes Cluster

## Downloading the Zerto Operations Help Utility
