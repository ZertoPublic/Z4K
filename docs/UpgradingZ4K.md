# Upgrading Z4K

To upgrade the Z4K solution you must first upgrade the Zerto Kubernetes Management (ZKM) site and then upgrade the Zerto Kubernetes Manager Proxy (ZKM-PX) site.

###### Upgrading the ZKM Site
    
Use the following commands to get the release name and then upgrade.

```
➜**>helm list -n <namespace>**
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
<release name>  <namespace>     1               2022-09-07 09:16:04.896907435 +0300 IDT deployed        zkm-px-2.4.18+538       2.4.18+538

➜**>helm upgrade <release-name> <helm repository> -n <namespace>**

At the end you will recieve the following message:
Release "<release name>" has been upgraded. Happy Helming!
NAME: <release name>
LAST DEPLOYED: Wed Sep  7 09:26:31 2022
NAMESPACE: <namespace>
STATUS: deployed
REVISION: <revision number>
NOTES:
See the installed app by running these command:
kubectl get deployments -n <namespace>
```

###### Upgrading the ZKM-PX

Upgrade the ZKM-PX site **after** upgrading the ZKM site using the same commands to get the release name and then upgrade.

```
➜**>helm list -n <namespace>**
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
<release name>  <namespace>     1               2022-09-07 09:16:04.896907435 +0300 IDT deployed        zkm-px-2.4.18+538       2.4.18+538

➜**>helm upgrade <release-name> <helm repository> -n <namespace>**

At the end you will recieve the following message:
Release "<release name>" has been upgraded. Happy Helming!
NAME: <release name>
LAST DEPLOYED: Wed Sep  7 09:26:31 2022
NAMESPACE: <namespace>
STATUS: deployed
REVISION: <revision number>
NOTES:
See the installed app by running these command:
kubectl get deployments -n <namespace>
```

