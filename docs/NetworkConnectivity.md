# Troubleshooting Network Connectivity

When the ZVM-PX id installed on another cluster the the following error is returned from “kubectl get sites“ command :
“error: the server doesn't have a resource type "sites"“ 
When the ZVM-PX is installed on the main site, and “kubectl get sites“ command returns only the current site

Use the following procedure to verify the ZKM-PX installation parameters.

1.  Validate connectivity to the provided external IP:

    -  ZKeyckloak component:

>>``
>>curl -I -k https://<EXTERNAL_IP>/auth -H "HOST: zkm.z4k.zerto.com"
>>``

    -  ZKM component:

    ``
    curl -I -k https://<EXTERNAL_IP>/zkm/api/help/index.html -H "HOST: zkm.z4k.zerto.com"
    ``

2.  Switch to ZKM-PX site, and validate the ZKM connectivity:

    ``
    kubectl run curltest --image=yauritux/busybox-curl --restart=Never -i --rm -- /bin/curl -I -k https://<EXTERNAL_IP>/zkm/api/help/index.html -H "HOST:           zkm.z4k.zerto.com" 
    ``

    Check which error code is returned.

3. Check the ZKeyckloak connectivity:

``
curl -I -k https://<EXTERNAL_IP>/auth -H "HOST: zkm.z4k.zerto.com"
``

Check which error code is returned.


 

