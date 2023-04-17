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

3. To run the tool and provide the required parameters when prompted:
   
   - To deploy ZKM and ZKM-PX on the current cluster, run:
    
     ```
     ./install-z4k.sh
     ```
     
    - To deploy only ZKM-PX on the current cluster, run:
    
        ```
        ./install-zkm-px.sh 
        ```
    OR
    
    To run the tool and provide parameters using the dedicated flags:
   
     - Add --help to the command to view the flags.
          
        ```
        ./install-z4k.sh --help
         Flags:
               --keycloakUser                 Keycloak administrator user name
               --keycloakPassword             Keycloak administrator password
               --manUser                      Keycloak management user name
               --manPassword                  Keycloak management password
               --secret                       Image pull secret
               --license                      Application license key
               --site                         A unique site name
               --release                      An easy to recognize release name
               --namespace                    A dedicated Zerto namespace (default: zerto)
               --openshift                    Are you installing on Openshift (0/1)
               --installIngress               Do you want to install a dedicated ingress (0/1)
               --repolink                     Helm Repository name (default: zerto-z4k/z4k)
               -h, --help                     Help for z4k-installer
           ```
    
   
           ```
           install-zkm-px.sh --help
           Flags:
                  --manUser                   Keycloak management user name
                  --manPassword               Keycloak management password
                  --secret                    Image pull secret
                 --site                       A unique site name
                 --release                    An easy to recognize release name
                 --namespace                  A dedicated Zerto namespace (default: zerto)
                 --externalIp                 Ingress service external IP (of main cluster)
                 --openshift                  Are you installing on Openshift? (0/1)
                 --installIngress             Do you want to install a dedicated ingress? (0/1)
                 --tag                        Tag image (default: latest)
                 --repolink                   Helm Repository name (default: zerto-z4k/zkm-px)
                 -h, --help                   Help for z4k-installer
            ```
