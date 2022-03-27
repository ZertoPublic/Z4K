# Z4K open API
In order to access the Z4K API please run the kubectl command:

```
kubectl get services -n <z4k namespace>
```

```
NAME                                              TYPE           CLUSTER-IP       EXTERNAL-IP                                                                 PORT(S)                               AGE
<release-name>-ingress-nginx-controller           LoadBalancer   XXX.XXX.XXX.XXX   @@ a11ed2fcc9d734cf594793d044753d97-1234567.eu-central-1.elb.amazonaws.com @@   80:31329/TCP,443:32363/
```

Type this EXTERNAL-IP in the browser and add the /zkm/api/help:
```
 https://a11ed2fcc9d734cf594793d044753d97-1234567.eu-central-1.elb.amazonaws.com/zkm/api/help

```

!!zswagger api.json!!
