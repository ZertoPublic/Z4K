# Uninstalling Z4K

To uninstall Z4K you must first uninstall the Zerto Kubernetes Manager Proxy (ZKM-PX) site and then uninstall the Zerto Kubernetes Management (ZKM) site.

#### Uninstalling ZKM-PX
    
Use the following commands to get the release name and then use it to uninstall.
    ```
    ➜>helm list -n <namespace>
    NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
    <release name>  <namespace>     1               2022-09-07 09:16:04.896907435 +0300 IDT deployed        zkm-px-2.4.18+538       2.4.18+538

    ➜>helm uninstall <release name> -n <namespace>
    ```

#### Uninstalling ZKM Site

1. Verify that you're on the ZKM cluster.
2. Use the following commands to get the release name and then use it to uninstall.

    ```   
    ➜**>helm list -n <namespace>**
    NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
    <release name>  <namespace>     2               2022-09-06 17:15:35.959682086 +0300 IDT deployed        z4k-2.4.18+538  2.4.17+478

    ➜**>helm uninstall <release name> -n <namespace>**
    ```
