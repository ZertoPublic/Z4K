# Configuring Virtual Protection Groups

Virtual machines are protected in virtual protection groups (VPG).  A VPG is a group of virtual machines that you group together for consistent protection and recovery purposes.

#### Configuring a VPG

1. Create a .yaml file to represent a VPG.
	In the following example the VPG webApp1:
   -	Is configured to self replicate to its source cluster.
   -	Will use the storage class goldSC.
   -	SLA is 12 hours of history.
   -	The Journal can expand up to 160 GB to meet the history requirement.

<span class="Note">Note:	It is not mandatory to configure the Journal disk size (JournalDiskSizeInGb) and history (JournalHistoryInHours); they have default values of 2 GB and 8 hours respectively.</span>
        
``` yaml
--- 
apiVersion: z4k.zerto.com/v1
kind: vpg
spec: 
  JournalDiskSizeInGb: 160
  JournalHistoryInHours: 12
  Name: “webApp1”
  RecoveryStorageClass: GoldSC
  SourceSite: 
    Id: prod_site
  TargetSite: 
    Id: dr_site
```


2. Annotate Kubernetes entities to include them in the VPG.
	-	A VPG can contain a selection of entities like stateful sets, deployments, services, secrets and configmaps.
 	-	Applications consisting of several components with interdependencies (for example secrets and deployments), should all be tagged with the same VPG annotation in order for the Failover operation to succeed.
	-	To include an entity in a VPG, you must annotate the entity with the VPG name.

Use the following example of deployment protection for guidelines.


``` yaml
--- 
kind: Deployment
metadata: 
  annotations: 
    vpg: "webApp1 /<VPG name as configured in VPG.yaml>"
  labels: 
    app: debian
  name: debian
spec: 
  replicas: 1
  selector: 
    matchLabels: 
      app: debian
  spec: 
    containers: 
      - 
        image: 
          command: 
            - /usr/bin/tail
            - "-f"
            - /dev/null
          debian: stable
          volumeMounts: 
            - 
              mountPath: /var/gil1
              name: external1
        name: debian1
    volumes: 
      - 
        claimName: my-vol1-debian-5to6
        name: external1
        persistentVolumeClaim: ~
  template: 
    metadata: 
      labels: 
        app: debian

```

#### Updating Existing VPGs

If you need to update an existing VPG you must create a yaml file as you did to create the VPG,
with an additional section called "metadata" that contains the VPG name and the namespace ID, and run the update command.

Example yaml:

``` yaml
--- 
apiVersion: z4k.zerto.com/v1
kind: vpg
spec: 
  JournalDiskSizeInGb: 160
  JournalHistoryInHours: 12
  RecoveryStorageClass: GoldSC
  SourceSite: 
    Id: prod_site
  TargetSite: 
    Id: dr_site
metadata:  
  name: webApp1
  namespace: zerto
```

Run the update kubernetes command:

``` shell
kubectl apply -f vpg.yaml
```

#### Viewing VPG Status

To display the VPG status as well as an overview of which entities are protected within the VPG, the VPG’s SLA and its settings, run the command:

``` shell
kubectl get vpg
```

