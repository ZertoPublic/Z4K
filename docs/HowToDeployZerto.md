# How To: Deploy Zerto For Kubernetes

Perform the following procedures:

1.	[Prepare Helm](#preparing-helm)
2.	[Obtain the Image Pull Key Secret](#obtaining-the-image-pull-key-secret)
3.	Next, select one of the following installation procedures:
    -	[Install Zerto for Kubernetes on a Kubernetes Cluster](#installing-zerto-for-kubernetes-on-a-kubernetes-cluster)
    -   [Install Zerto Kubernetes Manager Proxy on Additional Kubernetes Clusters](#installing-zerto-kubernetes-manager-proxy-on-additional-kubernetes-clusters)
    -	[Installing Zerto Kubernetes Manager on a Kubernetes Cluster](#installing-zerto-kubernetes-manager-on-a-kubernetes-cluster)
4.	[Downloading the Zerto Operations Help Utility](#downloading-the-zerto-operations-help-utility)

## Preparing Helm

On the Kubernetes platform, enter the following commands:

```
helm repo add zerto-z4k https://zapps-helm.zerto.com/z4k/stable
helm repo update
```

<span class="Note">Note: Helm name (in the example above, zerto-z4k) should be a logical name entered by the user.</span>

## Obtaining the Image Pull Key Secret

1.	Go to [myZerto](https://www.zerto.com/myzerto/).
2.	If required, log in using your myZerto credentials.
3.	Navigate to [Support & Downloads > Software Downloads > Zerto for K8s](https://www.zerto.com/myzerto/support/downloads/#z4k), and click **Generate Registry Key**.
4.	Copy the Registry Key. You will need it later when installing the Zerto software.

![PullKey](Images/PullKey.png?raw=true)

## Installing Zerto for Kubernetes on a Kubernetes Cluster

This installation includes the following components:

-	Zerto Kubernetes Manager (ZKM)
-	Zerto Kubernetes Manager Proxy (ZKM-PX)

Use either of these options to install Zerto for Kubernetes on any of the Zerto supported Kubernetes platforms.

### Option 1

Enter the following command, replacing the "$" variables with values relevant to your deployment.
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

### Option 2
1.	Create the following values.yaml:
>    ```
>     global:
>       authentication:
>         adminPassword: $ADMIN_PASSWORD
>         adminUser: $ADMIN_USER
>        managementPassword: $KEYCLOAK_PASSWORD
>        managementUser: $KEYCLOAK_USER
>        imagePullSecret: $IMAGE_PULL_KEY
>    zkm-px:
>      config:
>        siteId: $SITE
>    ```
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
Therefore, to enable VRA communication, you must disable ingress deployment and provide the external IP of the sites.


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

This installation includes the following components:
-	Zerto Kubernetes Manager Proxy (ZKM-PX)

Perform these steps:

1.	[Get an initial access token from Keycloak](#getting-an-initial-access-token-from-keycloak)
2.	[Install Zerto Kubernetes Manager Proxy on Additional Clusters](#installing-zerto-kubernetes-manager-proxy-on-additional-clusters)

## Getting an initial access token from Keycloak
Before you can begin to install Zerto Kubernetes Manager Proxy on additional Kubernetes clusters, you first need to get an initial access token from Keycloak, which was installed as part of ***z4k/zkm*** installation.

Creating an initial access token can be achieved in one of two ways:

### Creating an Initial Access Token - Option 1

<span class="Note">Note: Use this option only if two-factor authentication (2FA) is **not** enabled for the Keycloak management user.</span>
 
1.  Generate an initial access token via REST commands to Keycloak.
2.  Download and execute the following script:
```
wget https://z4k.zerto.com/public/generate_initial_access_token.bash
chmod +x generate_initial_access_token.bash
./generate_initial_access_token.bash
```
<span class="Note">Note: The URL should end with /auth.</span>

### Creating an Initial Access Token - Option 2

1.	Edit your hosts file so that **zkm.z4k.zerto.com** points to your load balancer address.
2.	Browse to Keycloak: [https://zkm.z4k.zerto.com/auth](https://zkm.z4k.zerto.com/auth)
>   ![Browse](Images/Keycloak_Option2_Browse.png?raw=true)
3.	Log in to the **Administration Console** using your **$KEYCLOAK_USER** and **$KEYCLOAK_PASSWORD**.
4.	Log in to Keycloak.
>   ![Sign In](Images/Keycloak_Option2_SignIn.png?raw=true)
5.	Select the **Realm Settings** option from the drop-down menu, and in the right pane, select the **Client Registration Policies** tab.
6.	Click **Create**.
>   ![Create](Images/Keycloak_Option2_InitialAccessToken_Create.png?raw=true)
7.	In the Add Initial Access Token panel, in the **Expiration** field define time-frame within which the token will expire in **Seconds/Minutes/Hours/Days**.
8.	In the **Count** field, define the token usage count.
>   ![Token Expiration](Images/Keycloak_Option2_TokenExpiration.png?raw=true)
9.	Click **Save** to generate and display a token.
>   ![Back](Images/Keycloak_Option2_InitialAccessToken_Back.png?raw=true)
10.	Save the token.
11.	Click **Back** to return to Keycloak.

## Installing Zerto Kubernetes Manager Proxy on Additional Clusters

Use either of these options to install Zerto Kubernetes Manager Proxy on additional clusters, on any of the Zerto supported Kubernetes platforms.

### Option 1
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

### Option 2    
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
    >   Where,
    >   | Parameter	| Description |
    >   | --------- | ------- | 
    >   |\<installation names\>	| Specify an easy to recognize name. |
    >   | $NAMESPACE | A dedicated Zerto namespace. We recommend using the namespace zerto. |
    In **OpenShift** on **VMware platforms**, Zerto does not deploy its own ingress controller but rather utilizes the built-in routes. Therefore, to enable VRA communication, you must disable ingress deployment and provide the external IP of the sites.

    
    **To disable ingress deployment and provide the external IP of the sites** enter the following commands:
    ```
    --set zkmProxyIngressControllerEnabled=false
    --set config.externalIp=$SITE_IP
    ```

## Installing Zerto Kubernetes Manager on a Kubernetes Cluster

Use one of these options to install the Zerto Kubernetes Manager (ZKM) on any of the Zerto supported Kubernetes platforms.

### Option 1

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
    
### Option 2 
    
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

**To disable ingress deployment** enter the following commands:

```
--set zkmIngressControllerEnabled=false
--set useNginxRoutePath=false
```


## Downloading the Zerto Operations Help Utility
    
-   Download the Help Utility so you can enter Zerto operations commands. This is a bash script wrapper for the kubectl API extension.
-   To use the Help Utility, first download then run the command 
    ```kubectl-zrt```
-   To run Zerto operation commands, on the Kubernetes platform enter the following commands:

```
wget https://z4k.zerto.com/public/kubectl-zrt
chmod +x kubectl-zrt
sudo cp kubectl-zrt /usr/bin/
```

<span class="Note">Note: If kubectl-zrt is not installed in /usr/bin, you must point to the relevant location.</span>

-   To view all Zerto commands, run 
    ```kubectl-zrt –```

    >   ![kubectl-zrt](Images/Z4K_Kubernetes_Commands.png?raw=true)
