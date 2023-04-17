# Z4K Installer

Zerto provides a Z4K Installer tool to simplify the Z4K installation process. You can use it to install a complete Z4K site with Zerto Kubernetes Manager (ZKM) and Zerto Kubernetes Manager Proxy (ZKM-PX), or a site with ZKM-PX only. It deploys all required components and verifies the installation.

1. Download the z4k-installer.tar file using wget:

    ```
    wget https://z4k.zerto.com/z4k-installer.tar
    ```

2. Extract all files:

    ```
    tar -xvf z4k-installer.tar
    ```

3. Run the tool.
   
   - To deploy ZKM and ZKM-PX on the current cluster, and provide the required parameters when prompted:
    
     ```
     ./install-z4k.sh
     ```
     
   - To deploy only ZKM-PX on the current cluster, and provide the required parameters when prompted:
    
      ```
      ./install-zkm-px.sh 
      ```
    OR
    
    To deploy ZKM and/or ZKM-PX on the current cluster and provide parameters with dedicated flags: 
    -  Run the command with --help to see what flags are valid.
    -  Run the command with the flags.

    **Example**
   
          
          install-zkm-px.sh --help
          
           Flags:
                --manUser                    Keycloak management user name
                --manPassword                Keycloak management password
                --secret                     Image pull secret
                --site                       A unique site name
                --release                    An easy to recognize release name
                --namespace                  A dedicated Zerto namespace (default: zerto)
                --externalIp                 Ingress service external IP (of main cluster)
                --openshift                  Are you installing on Openshift? (0/1)
                --installIngress             Do you want to install a dedicated ingress? (0/1)
                --tag                        Tag image (default: latest)
                --repolink                   Helm Repository name (default: zerto-z4k/zkm-px)
                -h, --help                   Help for z4k-installer
           
          
           ./install-zkm-px.sh --keycloakUser USERKEY  --keycloakPassword A1bcD345
                    
