# Z4K Deployment

Perform the procedures in the following order:

1.	Prepare Helm
2.	Obtain the Image Pull Key Secret
3.	Configure the Ingress Controller
4.	Install the Zerto for Kubernetes Components
    - Install Zerto for Kubernetes
    -	Install Zerto Kubernetes Manager
    -	Create the Initial Access Token from Keycloak
    -	Install Zerto Kubernetes Manager Proxy
    - Install Z4K on Openshift
    - Install Z4K on OpenShift on Additional cluster
5.	Download the Zerto Operations Help Utility
6.	(When required) Update Z4K with a new Zerto License

#### Preparing Helm

On the Kubernetes platform, enter the following commands:

``` shell
helm repo add zerto-z4k https://zapps-helm.zerto.com/z4k/stable
helm repo update
```

<span class="Note">Note:	Helm name (in the example above, zerto-z4k) should be a logical name entered by the user.</span>

#### Obtaining the Image Pull Key Secret

1.	Go to [myZerto](https://www.zerto.com/myzerto/).
2.	If required, log in using your myZerto credentials.
3.	Navigate to [Support & Downloads > Software Downloads > Zerto for K8s](https://www.zerto.com/myzerto/support/downloads/#z4k), and click **Generate Registry Key**.
4.	Copy the Registry Key. You will need it later when installing the Zerto software.

![PullKey](Images/PullKey.png?raw=true)

#### Configuring the Ingress Controller

To configure the ingress controller with static IP, set the following flags in the value.yaml file as input for HELM during the installation:

##### Configuring the Ingress Controller for ZKM

``` shell
--set ingress-nginx.controller.service.loadBalancerIP=$STATIC_IP
```

##### Configuring the Ingress Controller for ZKM-PX only

``` shell
--set zkm-px.ingress-nginx.controller.service.loadBalancerIP=$STATIC_IP
```


#### Installing Zerto for Kubernetes Components

Installation includes installation of the following components:

-   Zerto for Kubernetes (Z4K)
-	Zerto Kubernetes Manager (ZKM)
-	Zerto Kubernetes Manager Proxy (ZKM-PX)




#### Installing Zerto for Kubernetes

Use either of these options to install Zerto for Kubernetes (Z4K) on any of the Zerto supported Kubernetes platforms.

<span class="Note">Note: For both options you can add the following flag to capture helm install logs for debugging and troubleshooting purposes: ```
--debug > <path_to_file>.txt```

    
##### Installing Z4K with a Command

Enter the following commands, replacing the "$" variables with values relevant to your deployment.
``` shell
helm install <installation names> zerto-z4k/z4k \
--set global.imagePullSecret=$IMAGE_PULL_KEY \
--set global.authentication.managementUser=$KEYCLOAK_USER
--set global.authentication.managementPassword=$KEYCLOAK_PASSWORD
--set global.authentication.adminUser=$ADMIN_USER
--set global.authentication.adminPassword=$ADMIN_PASSWORD
--set zkm-px.config.siteId=$SITE \
--namespace $NAMESPACE
```
Where,

    | Parameter | Description |
    | --------- | ----------- |
    | <installation names\> | Specify an easy to recognize name. |
    | $SITE |	A unique site name. |
    | $NAMESPACE | A dedicated Zerto namespace. Zerto recommends using the namespace 'zerto'. |
    

##### Installing Z4K with a Values YAML File
    
1.	Create the following values.yaml:

    ``` yaml
    --- 
    global: 
      imagePullSecret: $IMAGE_PULL_KEY
      authentication: 
        adminPassword: $ADMIN_PASSWORD
        adminUser: $ADMIN_USER
        managementPassword: $KEYCLOAK_PASSWORD
        managementUser: $KEYCLOAK_USER
    zkm-px: 
      config: 
        siteId: $SITE
    ```
    Where,</br>
    $SITE is a unique site name.
    
2. Install Z4K using the following command:

    ``` shell
    helm install <installation names> zerto-z4k/z4k -f values.yaml --namespace $NAMESPACE
    ```
    Where,

    | Parameter | Description |
    | --------- | ----------- |
    | <installation names\> | Specify an easy to recognize name. |
    | $NAMESPACE | A dedicated Zerto namespace. Zerto recommends using the namespace 'zerto'. |
    | $SITE |	A unique site name. |

<span class="Note">Note:
    The <installation name\> must consist of lower case alphanumeric characters or '-', 
    and must start and end with an alphanumeric character (e.g. 'my-name', or '123-abc', regex used for validation is 'a-z0-9?').</span>

  

#### Installing Zerto Kubernetes Manager

Use one of these options to install the Zerto Kubernetes Manager (ZKM) on any of the Zerto supported Kubernetes platforms.

##### Installing ZKM with Commands

Enter the following commands, replacing the "$" variables with values relevant to your deployment.

``` shell
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
| <installation names\> |	Specify an easy to recognize name. |
| $NAMESPACE |	A dedicated Zerto namespace. We recommend using the namespace zerto. |
    
##### Installing ZKM with a Values YAML File
    
1.  Create the following values.yaml:

    ``` yaml
    --- 
    global: 
      authentication: 
        adminPassword: $ADMIN_PASSWORD
        adminUser: $ADMIN_USER
        imagePullSecret: $IMAGE_PULL_KEY
        managementPassword: $KEYCLOAK_PASSWORD
        managementUser: $KEYCLOAK_USER
    ``` 

2. Install ZKM using the following command:  

    ```
    helm install <installation names> zerto-z4k/zkm -f values.yaml –namespace $NAMESPACE
    ```
    Where,</br>
    $NAMESPACE is a dedicated Zerto namespace. We recommend using the namespace zerto..

#### Creating the Initial Access Token using Keycloak

KeyCloak is installed during the ZKM installation. Before you can begin to install Zerto Kubernetes Manager Proxy (ZKM-PX) on additional Kubernetes clusters, you must create an initial access token using Keycloak.

Use one of the following processes depending on where you have or have not enabled two-factor authentication (2FA) for the Keycloak management user.

##### If 2FA is Enabled for Keycloak Management User

Use this option to create the initial access token if two-factor authentication (2FA) is enabled for the Keycloak management user.

1.	Edit your hosts file so that **zkm.z4k.zerto.com** points to your load balancer address.
2.	Browse to Keycloak: [https://zkm.z4k.zerto.com/auth](https://zkm.z4k.zerto.com/auth)
>   ![Browse](Images/Keycloak_Option2_Browse.png?raw=true)
3.	Log in to the **Administration Console** using your **$KEYCLOAK_USER** and **$KEYCLOAK_PASSWORD**.
4.	Log in to Keycloak.
>   ![Sign In](Images/Keycloak_Option2_SignIn.png?raw=true)
5.	Select the **Realm Settings** option from the drop-down menu, and in the right pane, select the **Client Registration** tab.
6.	Click **Create**.
>   ![Create](Images/Keycloak_Option2_InitialAccessToken_Create.png?raw=true)
7.	In the Add Initial Access Token panel, in the **Expiration** field define time-frame within which the token will expire in **Seconds/Minutes/Hours/Days**.
8.	In the **Count** field, define the token usage count.
>   ![Token Expiration](Images/Keycloak_Option2_TokenExpiration.png?raw=true)
9.	Click **Save** to generate and display a token.
>   ![Back](Images/Keycloak_Option2_InitialAccessToken_Back.png?raw=true)
10.	Save the token.
11.	Click **Back** to return to Keycloak.

##### If 2FA is Disabled for Keycloak Management User

Use this option to create the initial access token only if 2FA is disabled for the Keycloak management user.
 
1.  Generate an initial access token via REST commands to Keycloak.
2.  Download and execute the following script:
``` shell
wget https://z4k.zerto.com/generate_initial_access_token.bash
chmod +x generate_initial_access_token.bash
./generate_initial_access_token.bash
```
<span class="Note">Note**:	The URL should end with /auth</span>


#### Installing Zerto Kubernetes Manager Proxy

1. Create the initial access token using keycloak
2. Install Zerto Kubernetes Manager Proxy (ZKM-PX) on any of the Zerto supported Kubernetes platforms using one of the following options.

##### Installing ZKM-PX Using Commands

Enter the following commands to install Zerto Kubernetes Manager Proxy:

``` shell
helm install <installation name> zerto-4k/zkm-px \
--set global.imagePullSecret=$IMAGE_PULL_KEY \
--set global.authentication.initialAccessToken=$INITINAL_ACCESS_TOKEN
--set config.siteId=$SITE \
--set config.zkmUrl=$ZKM_URL \
--set config.zkeycloakUrl=$ZKEYCLOAK_URL \
--namespace $NAMESPACE
```
  Where,

| Parameter	| Description |
| --------- | ----------- |
| <installation names\>	| Specify an easy to recognize name. |
| $SITE |	A unique site name. |
| $ZKM_URL |	URL for ZKM. Typically: "https://<load balancer addr>/zkm" |
| $ZKEYCLOAK _URL | URL for Keycloak. Typically: https://<load balancer addr>/auth |


##### Installing ZKM-PX Using a Values YAML File    

1. Create the following values.yaml:

    ``` yaml
    --- 
    config: 
      siteId: $SITE
      zkeycloakUrl: $ZKEYCLOAK_URL
      zkmUrl: $ZKM_URL
    global: 
      authentication: 
        imagePullSecret: $IMAGE_PULL_KEY
        initialAccessToken: $INITIAL_ACCESS_TOKEN
    ```
    
2.  Install ZKM-PX using the command:
    
    ```
    helm install <installation names> zerto-z4k/zkm-px -f values.yaml --namespace $NAMESPACE
    ```
 
    Where,

    | Parameter  | Description |
    | ---------  | ----------- | 
    | <installation names\>  | Specify an easy to recognize name. |
    | $NAMESPACE  | A dedicated Zerto namespace. We recommend using the namespace zerto. |
    

#### Installing Z4K on OpenShift

In **OpenShift on VMware platforms**, Zerto does not deploy its own ingress controller but rather utilizes the built-in routes.
Therefore, to enable VRA communication, you must disable ingress deployment and provide the external IP of the sites.

**To disable ingress deployment and provide the external IP of the sites** enter the following commands:
``` shell
--set zkm.zkmIngressControllerEnabled=false
--set zkm-px.zkmProxyIngressControllerEnabled=false
--set zkm-px.config.externalIp=$SITE_IP
--set zkm.useNginxRoutePath=false
```

#### Setting Custom Ingress Class Names

To find the default ingress class name, run the command:

```kubectl get ingressclass```

Use the following flags to specify the used IngressClassNames:

``` shell
helm install z4k zerto-z4k/z4k \
--set zkm-px.image.zkmPxRepository=zapps-registry.zerto.com/z4k/stable/zkm-px \
--set zkm-px.image.flowsRepository=zapps-registry.zerto.com/z4k/stable/zkm-installer-flows \
--set zkm-px.config.siteId=$SITE \
--set zkm.image.zkmRepository=zapps-registry.zerto.com/z4k/stable/zkm \
--set zkm.image.coreRepository=zapps-registry.zerto.com/z4k/stable/zkm-core \
--set zkm.client.licenseKey=$LICENSEKEY
--set global.authentication.managementUser=$KEYCLOAK_USER \
--set global.authentication.managementPassword=$KEYCLOAK_PASSWORD \
--set global.authentication.adminUser=$ADMIN_USER \
--set global.authentication.adminPassword=$ADMIN_PASSWORD \
--set global.imagePullSecret=$IMAGEPULLSECRET \
--set zkm.zkmIngressControllerEnabled=false \
--set zkm-px.zkmProxyIngressControllerEnabled=false \
--set zkm-px.config.externalIp=$EXTERNALIP \
--set zkm.useNginxRoutePath=false \
--set zkm-px.vras.ingressClass=$INGRESSCLASSNAMES \
--set zkm-px.ingress-nginx.controller.ingressClass=$INGRESSCLASSNAMES \
--set zkm.ingress-nginx.controller.ingressClass=$INGRESSCLASSNAMES \
--set zkm.ingress.annotations.kubernetes\\.io/ingress\\.class=$INGRESSCLASSNAMES \
--set zkm.zkeycloak.ingress.annotations.kubernetes\\.io/ingress\\.class=$INGRESSCLASSNAMES \
--namespace $NAMESPACE
```

#### Installing Z4K on OpenShift on an Additional Cluster

``` shell
helm install z4k zerto-z4k/zkm-px \
--set global.authentication.initialAccessToken=$INITIALACCESSTOKEN \
--set global.imagePullSecret=$IMAGEPULLSECRET \
--set config.siteId=$SITE \
--set config.zkmUrl=$ZKMURL \
--set config.zkeycloakUrl=$ZKEYCLOAKURL
--set zkmProxyIngressControllerEnabled=false \
--set vras.ingressClass=$INGRESSCLASSNAMES \
--set ingress-nginx.controller.ingressClass=$INGRESSCLASSNAMES \
--set config.externalIp=$externalIp --namespace $NAMESPACE
```


#### Downloading the Zerto Operations Help Utility
    
-   Download the Help Utility so you can enter Zerto operations commands. This is a bash script wrapper for the kubectl API extension.
-   To use the Help Utility, first download then run the command:
    ```kubectl-zrt```
-   To run Zerto operation commands, on the Kubernetes platform enter the following commands:

``` shell
wget https://z4k.zerto.com/kubectl-zrt
chmod +x kubectl-zrt
sudo cp kubectl-zrt /usr/bin/
```

<span class="Note">Note:	If kubectl-zrt is not installed in /usr/bin, you must point to the relevant location.</span>

-   To view all Zerto commands, run 
    ```kubectl-zrt –```

    >   ![kubectl-zrt](Images/Z4K_Kubernetes_Commands.png?raw=true)

#### Updating Z4K with a New Zerto License
    
To update Z4K with a new Zerto license, run the following command with the relevant environment variables:
    
```
kubectl set env deployment/<zkm-deploy-name> LICENSE_KEY=<new_license> -n <namespace>
```

To verify the new license has been successfully updated, run the following command and go to the deployment description under the Environment variable LICENSE_KEY:

```
kubectl describe deployments.apps <deply-zkm-name> -n <zerto-namespace>
```
