# Network Connectivity

#### Symptoms

-   When the ZVM-PX is installed on another cluster, the command ```kubectl get sites``` returns the error ```Error: the server doesn't have a resource type "sites"```

-   When the ZVM-PX is installed on the main site, the ```kubectl get sites``` command returns only the current site.

#### Root Cause

@Yuri

#### Solution

Use the following procedure to verify the ZKM-PX installation parameters, after successfully installing ZKM and **before** installing ZKM-PX on a new cluster.

1.  Validate connectivity to the provided external IP.

    -  Keycloak connectivity:

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

        ** This command will create a pod - run curl command and destroy the pod when done ** 

        Success code = 200. If you get an error code (i.e, 400, 404) handle your connectivity issue accordingly. 

    -   Keycloak connectivity:

        ```
        kubectl run curltest --image=yauritux/busybox-curl --restart=Never -i --rm -- /bin/curl -I -k https://<EXTERNAL_IP>/auth/realms/master -H "HOST: zkm.z4k.zerto.com
        ```

        ** This command will create a pod - run curl command and destroy the pod when done ** 

        Success code = 200. If you get an error code (i.e, 400, 404) handle your connectivity issue accordingly. 

<span class="Note">Note: You can also run the script **zkm-px-troubleshooting.sh** which is available as part of the z4k-installer.tar file.</span>
