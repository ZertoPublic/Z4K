# How To: Deploy Zerto For Kubernetes


Perform the following procedures:

1.	[Prepare Helm](#Preparing-Helm)
2.	[Obtain the Image Pull Key Secret](#Obtaining-the-Image-Pull-Key-Secret)
3.	Next, select one of the following installation procedures:
    -	[Install Zerto for Kubernetes on a Kubernetes Cluster](#Installing-Zerto-for-Kubernetes-on-a-Kubernetes-Cluster)
    -   [Install Zerto Kubernetes Manager Proxy on Additional Kubernetes Clusters](#Installing-Zerto-Kubernetes-Manager-Proxy-on-Additional-Kubernetes-Clusters)
    -	[Installing Zerto Kubernetes Manager on a Kubernetes Cluster](#Installing-Zerto-Kubernetes-Manager-on-a-Kubernetes-Cluster)
4.	[Downloading the Zerto Operations Help Utility](#Downloading-the-Zerto-Operations-Help-Utility)

## Preparing Helm

On the Kubernetes platform, enter the following commands:

```
helm repo add zerto-z4k https://zapps-helm.zerto.com/z4k/stable
helm repo update
```

> Note:	Helm name (in the example above, zerto-z4k) should be a logical name entered by the user.

## Obtaining the Image Pull Key Secret

1.	Go to [myZerto](https://www.zerto.com/myzerto/).
2.	If required, log in using your myZerto credentials.
3.	Navigate to [Support & Downloads > Software Downloads > Zerto for K8s](https://www.zerto.com/myzerto/support/downloads/#z4k), and click **Generate Registry Key**.
4.	Copy the Registry Key. You will need it later when installing the Zerto software.

![PullKey](Images/PullKey.png?raw=true)

## Installing Zerto for Kubernetes on a Kubernetes Cluster

This installation includes the following:

-	Zerto Kubernetes Manager (ZKM)
-	Zerto Kubernetes Manager Proxy (ZKM-PX)

Use the following commands to install Zerto for Kubernetes on any of the Zerto supported Kubernetes platforms.

Enter the following commands:

> Note: Replace "$" variables with values relevant to your deployment.

```
helm install <installation names> zerto-z4k/z4k \
--set global.imagePullSecret=$IMAGE_PULL_KEY \
--set global.authentication.managementUser=$KEYCLOAK_USER
--set global.authentication.managementPassword=$KEYCLOAK_PASSWORD
--set global.authentication.adminUser=$ADMIN_USER
--set global.authentication.adminPassword=$ADMIN_PASSWORD
--set zkm-px.config.siteId=$SITE \
--namespace $NAMESPACE
```

**-OR-**


1.	Create the following values.yaml:

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

2. Install using the following command:

```
helm install <installation names> zerto-z4k/z4k -f values.yaml --namespace $NAMESPACE
```
Where,

| Parameter | Description |
| --------- | ------- |
| \<installation names\> | Specify an easy to recognize name. |
| $NAMESPACE | A dedicated Zerto namespace. Zerto recommends using the namespace 'zerto'. |
| $SITE |	A unique site name. |


In **OpenShift on VMware platforms**, Zerto does not deploy its own ingress controller but rather utilizes the built-in routes.
As such, to enable VRA communication, you need to disable ingress deployment and provide the external IP of the sites.

**To disable ingress deployment and provide the external IP of the sites** enter the following commands:

```
--set zkm.zkmIngressControllerEnabled=false
--set zkm-px.zkmProxyIngressControllerEnabled=false
--set zkm-px.config.externalIp=$SITE_IP
--set zkm.useNginxRoutePath=false
```

If the IngressClassNames are not the default names, use the following flags to specify the used IngressClassNames:

```
--set zkm-px.vras.ingressClass=$ingressClassName
--set zkm-px.ingress-nginx.controller.ingressClass=$ingressClassName
--set zkm.ingress-nginx.controller.ingressClass=$ingressClassName
--set zkm.ingress.annotations.kubernetes\\.io/ingress\\.class=$ingressClassName
--set zkm.zkeycloak.ingress.annotations.kubernetes\\.io/ingress\\.class=$ingressClassName
```


## Installing Zerto Kubernetes Manager Proxy on Additional Kubernetes Clusters

This installation includes the following:

-	Zerto Kubernetes Manager Proxy (ZKM-PX)
1.	[Get an initial access token from Keycloak](#getting-an-initial-access-token-from-keycloak)
2.	[Install Zerto Kubernetes Manager Proxy on Additional Clusters](#installing-zerto-kubernetes-manager-proxy-on-additional-clusters)

## Getting an initial access token from Keycloak
Before you can begin to install Zerto Kubernetes Manager Proxy on additional Kubernetes clusters, you first need to get an initial access token from Keycloak, which was installed as part of ***z4k/zkm*** installation.

Creating an initial access token can be achieved in one of two ways:

### Creating Initial Access Token - Option 1

1.  Generate an initial access token via REST commands to Keycloak.

2.  Download and execute the following script.

> Note:	Do not run this script if two-factor authentication (2FA) was enabled for the Keycloak management user.


```
wget https://z4k.zerto.com/public/generate_initial_access_token.bash
chmod +x generate_initial_access_token.bash
./generate_initial_access_token.bash
```

> Note:	The url should end with /auth

### Creating Initial Access Token - Option 2


1.	Edit your hosts file so that **zkm.z4k.zerto.com** points to your load balancer address.
2.	Browse to Keycloak: [https://zkm.z4k.zerto.com/auth](https://zkm.z4k.zerto.com/auth)

>   [Browse](Images/Keycloak_Option2_Browse.png?raw=true)

3.	Login to the **Administration Console** using your **$KEYCLOAK_USER** and **$KEYCLOAK_PASSWORD**.

>   The Keycloak Zerto Realm page is diaplyed.

>   ![Sign In](Images/Keycloak_Option2_SignIn.png?raw=true)

4.	In the left pane, click **Realm Settings**, and in the right pane, select the **Client Registration** tab.
>   The Initial Access Tokens tab is displayed by default.

>   ![Zerto Realm](Images/Keycloak_Option2_ZertoRealm.png?raw=true)

5.	On the right side of the page, click **Create**.

>   ![Create](Images/Keycloak_Option2_InitialAccessToken_Create.png?raw=true)

6.	In the Add Initial Access Token panel, define an **Expiration** time-frame within which the token will expire in **Seconds/Minutes/Hours/Days**.
7.	In the **Count** field, define the token usage count.

![Token Expiration](Images/Keycloak_Option2_TokenExpiration.png?raw=true)

8.	Click **Save**.

> A token is generated and displayed

8.	Save the token and click **Back**.

![Back](Images/Keycloak_Option2_InitialAccessToken_Back.png?raw=true)


## Installing Zerto Kubernetes Manager Proxy on Additional Clusters

Use the following commands to install Zerto Kubernetes Manager Proxy on additional clusters, on any of the Zerto supported Kubernetes platforms.

Enter the following commands:

```
helm install <installation name> zerto-4k/zkm-px \
--set global.imagePullSecret=$IMAGE_PULL_KEY \
--set global.authentication.initialAccessToken =$INITINAL_ACCESS_TOKEN
--set config.siteId=$SITE \
--set config.zkmUrl=$ZKM_URL \
--set config.zkeycloakUrl=$ZKEYCLOAK_URL \
--namespace $NAMESPACE
```
>   Where,

>   | Parameter	| Description |
>   | --------- | ------- | 
>   |\<installation names\>	| Specify an easy to recognize name. |
>   | $SITE |	A unique site name. |
>   | $ZKM_URL |	URL for ZKM. Typically: https://<load balancer addr>/zkm |
>   | $ZKEYCLOAK _URL | URL for Keycloak. Typically: https://<load balancer addr>/auth |

**-OR-**

1. Create the following values.yaml:

```
global:
  authentication:
    initialAccessToken: $INITIAL_ACCESS_TOKEN
    imagePullSecret: $IMAGE_PULL_KEY
config:
  siteId: $SITE
  zkmUrl: $ZKM_URL
  zkeycloakUrl: $ZKEYCLOAK_URL
```

2.  Install using the following command:
```
helm install <installation names> zerto-z4k/zkm-px -f values.yaml --namespace $NAMESPACE
```

Where,

| Parameter	| Description |
| --------- | ------- | 
|\<installation names\>	| Specify an easy to recognize name. |
| $NAMESPACE | A dedicated Zerto namespace. We recommend using the namespace zerto. |

In **OpenShift** on **VMware platforms**, Zerto does not deploy its own ingress controller but rather utilizes the built-in routes. Therefore, to enable VRA communication, you must disable ingress deployment and provide the external IP of the sites.

**To disable ingress deployment and provide the external IP of the sites** enter the following commands:

```
--set zkmProxyIngressControllerEnabled=false
--set config.externalIp=$SITE_IP
```

## Installing Zerto Kubernetes Manager on a Kubernetes Cluster

Use one of these steps to install the Zerto Kubernetes Manager (ZKM) on any of the Zerto supported Kubernetes platforms.

Enter the following commands:

```    
helm install <installation name> zerto/zkm \
--set global.imagePullSecret=$IMAGE_PULL_KEY \
--set global.authentication.managementUser=$KEYCLOAK_USER
--set global.authentication.managementPassword =$KEYCLOAK_PASSWORD
--set global.authentication.adminUser =$ADMIN_USER
--set global.authentication.adminPassword =$ADMIN_PASSWORD
--namespace $NAMESPACE
```
    
Where,

| Parameter |	Description |
| --------- | --------- |
| \<installation names\> |	Specify an easy to recognize name. |
| $NAMESPACE |	A dedicated Zerto namespace. We recommend using the namespace zerto. |
    
**-OR-** 
    
1.  Create the following values.yaml:

```
global:
  authentication:
    adminPassword: $ADMIN_PASSWORD
    adminUser: $ADMIN_USER
    managementPassword: $KEYCLOAK_PASSWORD
    managementUser: $KEYCLOAK_USER
    imagePullSecret: $IMAGE_PULL_KEY
```
    
2. Install using the following command:
    
```
helm install <installation names> zerto-z4k/zkm -f values.yaml –namespace $NAMESPACE
```
    
In **OpenShift** on **VMware platforms**, Zerto does not deploy its own ingress controller but rather utilizes the built-in routes. Therefore, to enable VRA communication, you need to disable ingress deployment.

**To disable ingress deployment** enter the following command:

```
--set zkmIngressControllerEnabled=false
--set useNginxRoutePath=false
```


## Downloading the Zerto Operations Help Utility
    
-   To facilitate entering of Zerto operations commands, download the Help Utility. This is a bash script wrapper for the kubectl API extension.

-   To use the Help Utility, you first download then run the command, kubectl-zrt.

-   To facilitate Zerto operation commands, on the Kubernetes platform, enter the following commands:

```
wget https://z4k.zerto.com/public/kubectl-zrt
chmod +x kubectl-zrt
sudo cp kubectl-zrt /usr/bin/
```

> Note: In case kubectl-zrt is not installed in /usr/bin, you need to point it to the relevant location.

-   To view all Zerto commands, run kubectl-zrt –

![kubectl-zrt](Images/Z4K_Kubernetes_Commands.png?raw=true)
