# Network Connectivity

#### Issues

-   When the ZVM-PX is installed on another cluster, the command ```kubectl get sites``` returns the error ```Error: the server doesn't have a resource type "sites"```

-   When the ZVM-PX is installed on the main site, the ```kubectl get sites``` command returns only the current site.

#### Procedure

Use the following procedure to verify the ZKM-PX installation parameters.

1.  Validate connectivity to the provided external IP.

    -  ZKeycloak connectivity:

       ```
        curl -I -k https://<EXTERNAL_IP>/auth -H "HOST: zkm.z4k.zerto.com    
        ```

    -  ZKM connectivity:

        ```
        curl -I -k https://<EXTERNAL_IP>/zkm/api/help/index.html -H "HOST: zkm.z4k.zerto.com
        ```

2.  Switch to the ZKM-PX site and validate connectivity:

    -  ZKM connectivity:
          
       ```
        kubectl run curltest --image=yauritux/busybox-curl --restart=Never -i --rm -- /bin/curl -I -k https://<EXTERNAL_IP>/zkm/api/help/index.html -H "HOST: zkm.z4k.zerto.com 
       ```

        Check which error code is returned.

    -   Keycloak connectivity:

        ```
        kubectl run curltest --image=yauritux/busybox-curl --restart=Never -i --rm -- /bin/curl -I -k https://<EXTERNAL_IP>/auth/realms/master -H "HOST: zkm.z4k.zerto.com
        ```

        Check which error code is returned.


 

