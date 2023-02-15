# Administration

After deploying Zerto for Kubernetes, create a VPG, optionally configure one-to-many, tag checkpoints, and then test failover:

1.	Create a VPG
2.	Configure One-to-Many
3.	Tag a Checkpoint
4.	Test Failover

Then, you can perform one of the following:

-	Perform a Failover
-	Restore a Single VPG
-	Configure an Extended Journal Copy repository in Kubernetes environments
	Zerto for Kubernetes supports backing up Kubernetes workloads and their data to an Extended Journal Copy and restoring them from the Extended Journal Copy to the original site or to a different site or namespace.
-	Protect Ingress Controller Resources
	Zerto for Kubernetes supports replicating Ingress Controller Resources so networking configuration can be replicated and easily deployed on the recovery site.
-	Taints and Tolerations
	Z4K supports taints and tolerations configuration for nodes and pods.


#### Creating a VPG


1. Create a .yaml file to represent a VPG. 
 	The following example shows VPG webApp1 configured as follows:

	- VPG webApp1 will self replicate to its source cluster.
	- VPG webApp1 Will use the storage class goldSC.
	- VPG webApp1's SLA is 12 hours of history.
	- VPG webApp1's journal can expand up to 160 GB to meet the history requirement.

>    ```
>	apiVersion: z4k.zerto.com/v1
>	kind: vpg
>	spec: 
>	  JournalDiskSizeInGb: 160
>	  JournalHistoryInHours: 12
>	  Name: “webApp1”
>	  RecoveryStorageClass: GoldSC
>	  SourceSite: 
>	    Id: prod_site
> 	 TargetSite: 
> 	   Id: dr_site
>     ```

><span class="Note">Note: It is not mandatory to configure the Journal disk size (JournalDiskSizeInGb) and history (JournalHistoryInHours); they have default values of 2 GB and 8 hours respectively.</span>

     
2. Annotate Kubernetes entities to include them in the VPG.

-	A VPG can contain a selection of entities like stateful sets, deployments, services, secrets and configmaps.

-	Applications consisting of several components with inter-dependencies (for example secrets and deployments), should all be tagged with the same VPG annotation in order for the Failover operation to succeed.
-	To include an entity in a VPG, you must annotate the entity with the VPG name.

Use the following example of deployment protection for guidelines.


```
kind: Deployment
metadata:
  name: debian
  labels:
    app: debian
  annotations:
    vpg: webApp1 /<VPG name as configured in VPG.yaml>
spec:
  replicas: 1
  selector:
    matchLabels:
      app: debian
  template:
    metadata:
      labels:
        app: debian
    spec:
      containers:
        - name: debian1
          image: debian:stable
	  command: ["/usr/bin/tail","-f","/dev/null"]
	  volumeMounts:
	  - mountPath: "/var/gil1"
	    name: external1
      volumes:
        - name: external1
	  persistentVolumeClaim:
	    claimName: my-vol1-debian-5to6
```

#### Configuring One-to-Many

Z4K can protect the same entity multiple times. 

The recommended configuration is to replicate no more than 3 VPGs (inbound & outbound). Exceeding this configuration is possible, bearing in mind that performance degradation may appear if POD/Cluster resources are being overutilized.

One-to-Many serves two main goals:
1.	Enables high availability (HA) for protected VPGs.
2.	Enables Continuous Data Protection (CDP) during migration with a local and a remote copy.

To protect the same entity multiple times:

- Add all of the VPG names in the annotation field with a ';' delimiter sign:

```
kind: Deployment
metadata:
  name: debian
  labels:
    app: debian
  annotations:
    vpg: webApp1Self; webApp1Site2; webApp1Site3 /<VPG names as configured in VPG yaml files>
    * * *
```   

- Create the VPG by running the command:


```
kubectl create -f vpg.yaml
```

##### Viewing VPG Status

To display the VPG status as well as an overview of which entities are protected within the VPG, the VPG’s SLA and it's settings, run the command:


```
kubectl get vpg
```


#### Tagging a Checkpoint

To tag a checkpoint, run the command:

```
kubectl zrt tag [vpg-name] [tag-name]
```

##### Displaying Available Checkpoints

-	To display a list of all available checkpoints for a VPG, including properties like the checkpoint ID, run the command:


```
kubectl get checkpoints --selector="vpg=vpgs;minAge=5m;maxAge=3d"
```

Where:

| Parameter |	Value |	Mandatory Y/N |
| --------- | ----- | ------------- |
| vpg       |	VPG name |	Y |
| minAge    | Minutes: m (example: 5m), Hours: h (example: 5h) , Days: d (example: 5d) | N |
| maxAge    | Minutes: m (example: 5m), Hours: h (example: 5h) , Days: d (example: 5d) | N |


#### Testing Failover

-	To test failover, run the command:

```
kubectl zrt failover-test [vpg-name] [checkpoint-id]
```

>Where [checkpoint ID] can be either an ID, or enter "latest" for the latest checkpoint.

-	To stop the test run, run the command:

```
kubectl zrt stop-test [vpg-name]
```

#### Performing a Failover
	
-	To failover run the command:

```
kubectl zrt failover-live [vpg-name] [checkpoint-id]
```

>Where [checkpoint-id] can be either an ID, or enter "latest" for the latest checkpoint.

-	To commit the failover, run the command:

```
kubectl zrt commit [vpg-name]
```
	
-	To rollback the failover, run the command:

```
kubectl zrt rollback [vpg-name]
```
	
#### Restoring a Single VPG

On a single cluster deployment, only the restore and failover test operations are available. Failover is not available.

-	To restore a single VPG, run the command:

```
kubectl zrt restore [vpg-name] [checkpoint-id]
```
	
>Where [checkpoint-id] can be either an ID, or enter latest, for the latest checkpoint.

-	To commit the restore, run the command:


```
kubectl zrt commit-restore [vpg-name]
```

-	To rollback the restore, run the command:


```
kubectl zrt rollback-restore [vpg-name]
```
#### Move operation

The move operation moves the deployments to the recovery site without preserving the VPGs on the protected site.

There are 3 commands for different move operations:

1. Move - Start move live, test before committing
2. Commit-move - Commit move
3. Rollback-move - Roll back the Move test before committing

The following syntax is used for these move commands:

```
kubectl zrt move [vpg-name] [checkpoint ID]
```

If a checkpoint is not tagged, use the value 'latest'

After the command is run, the VPG state will be updated to StartingMove.

When the move operation is complete, the VPG status will be updated to MoveBeforeCommit.

```
kubectl zrt rollback-move [vpg-name]
```

The VPG in the protected site will go back into protecting state without being committed to the recovery site.

```
kubectl zrt commit-move [vpg-name]
```

The VPG status will be changed to CommittingMove.

When the operation has completed, the VPG will be committed and the deployment will now exist on the recovery site.

The VPG will be removed from the environment.


#### Extended Journal Copy Repositories in Kubernetes Environments

Zerto for Kubernetes supports backing up Kubernetes workloads and their data to an Extended Journal Copy and restoring them from the an Extended Journal Copy to the original site, or to a different site.

##### Supported Extended Journal Copy Repository Types

Zerto for Kubernetes supports two an Extended Journal Copy repository types:

- AWS S3
- Azure Blob Storage
	
To configure an Extended Journal Copy for your Kubernetes environment, use the following procedures:

1.	Back up the VPG
2.	Manually trigger a Backup
3.	Schedule an Extended Journal Copy
4.	Restore the VPG from an Extended Journal Copy



##### Backing up a VPG

To backup a VPG to a target Extended Journal Copy repository, create the VPG and update the VPG yaml file (vpg.yaml) with the the Extended Journal Copy repository type.

Use the following examples as guidelines.
  
**Example vpg.yaml File - Backing Up to AWS S3**
  
```
apiVersion: z4k.zerto.com/v1
kind: vpg
spec:
  Name: test_vpg
  SourceSite:
    Id: site1
  TargetSite:
    Id: site1
  RecoveryStorageClass: zgp2
  BackupSettings:
    IsCompressionEnabled: true  
    RepositoryInformation:
      BackTargetType: AmazonS3
      AwsBackupRepositoryInformation:
        Region: eu-centeral-1
	Bucket: mybucket
	CredentialSecretReference:
          Site:
            Id: site1
	  Id:
	    Name: mysecret
            NamespaceId:
	      NamespaceName: default
  
```

-	The AWS S3 access key and secret key should be captured as a Kubernetes secret, whose name appears in the vpg.yaml file. In the example above, this is "mysecret".
-	The secret must contain a data item for the AccessKey and a data item for the SecretKey, and can be created in any site to which Zerto Kubernetes Manager has access. In the example above, this is "site1".

**Example vpg.yaml File - Backing Up to Azure Blob Storage**
  
```
apiVersion: z4k.zerto.com/v1
kind: vpg
spec:
  Name: test_vpg
  SourceSite:
    Id: site1
  TargetSite:
    Id: site1
  RecoveryStorageClass: zgp2
  BackupSettings:
    IsCompressionEnabled: true
    RepositoryInformation:
      BackTargetType: AzureBlob
      AzureBackupRepositoryInformation:
	StorageAccountName: mystorageaccount
	DirectoryId: c659fda3-cf53-43ad-befe-776ee475dcf5
	CredentialSecretReference:
	  Site:
	    Id: site1
	  Id:
	    Name: mysecret
	    NamespaceId:
	      NamespaceName: default
```

-	The Azure application id and client secret should be captured as a Kubernetes secret, whose name appears in the vpg.yaml file. In the example above, this is "mysecret". 
-	The secret must contain a data item for the ApplicationId and a data item for the ClientSecret, and can be created in any site to which Zerto Kubernetes Manager has access. In the example above, this is "site1".


##### Manually Trigger a Backup 
	
You must manually trigger a backup to create a retention set.


-	To manually trigger a backup, run the command:

```
kubectl zrt ltr-backup [vpg-name] [checkpoint-id]
```

>	A backup task is triggered. When the task completes successfully, a retention set is created.


-	To access the generated retention set ID (backupset ID), run the command:

```
kubectl get backupset
```

##### Scheduling an Extended Journal Copy Backup

To schedule an Extended Journal Copy bakcup, add **SchedulingAndRetentionSettings** to the VPGs **BackupSettings**.

Use the following example as a guideline.

```
apiVersion: z4k.zerto.com/v1
kind: vpg
spec:
  Name: test_vpg
  SourceSite:
    Id: site1
  TargetSite:
    Id: site1
  RecoveryStorageClass: zgp2
  BackupSettings:
    IsCompressionEnabled: true	
    RepositoryInformation:
      BackTargetType: AmazonS3
      AwsBackupRepositoryInformation:
	Region: eu-centeral-1
	Bucket: mybucket
	CredentialSecretReference:
	  Site:
	    Id: site1
	  Id:
	    Name: mysecret
	    NamespaceId:
	      NamespaceName: default
  SchedulingAndRetentionSettings:
    PeriodsSettings:
    - PeriodType: Yearly
      Method: Full
      ExpiresAfterValue: 7
      ExpiresAfterUnit: Years
    - PeriodType: Monthly
      Method: Full
      ExpiresAfterValue: 12
      ExpiresAfterUnit: Months							
    - PeriodType: Weekly
      Method: Full
      ExpiresAfterValue: 4
      ExpiresAfterUnit: Weeks
    - PeriodType: Daily
      Method: Incremental
      ExpiresAfterValue: 7
      ExpiresAfterUnit: Days
```

###### Important Considerations for SchedulingAndRetentionSettings

-	There must be at least one Full Method.
-	There can be no more than one Incremental Method.
-	A Full Method cannot be followed by an Incremental Method. In other words, if there is a Full Method, it should be the last in the chain.
-	Zerto Kubernetes Manager schedules backups and expirations as needed.
	
##### Restoring a VPG from an Extended Journal Copy

To restore a VPG from an Extended Journal Copy, run the command:

```
kubectl zrt ltr-restore [backupset-id] [site-id] [storage-class] [namespace]
```

Where:

| Parameter |	Comment |
| --------- | ------- |
| site-id | Identifier of the site to which you want to restore. |
| storage-class | Storage class, with which persistent volumes for the restored data is created. |
| namespace | namespace in which you want the restored Kubernetes entities to be created. |

These parameters give you flexibility in restoring a VPG to the original site, or to a different site or namespace.
You can also restore from an Extended Journal Copy repository that has VPGs backup sets from a different site and restore them to a new site using the parameter backupset-id.
	
When the restore task completes successfully, Kubernetes entities with the prefix "res-" are created in the specified site and namespace.

#### Protecting Ingress Controller Resources

There are 2 options to configure Ingress Controller Resources with a deployment for protection:
	
- Configure protection when creating a new deployment, as defined in the YAML example below:

	>```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: minimal-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    vpg: website-vpg1
spec:
  ingressClassName: nginx-example
  rules:
  - http:
    paths:
    - path: /testpath
      pathType: Prefix
      backend:
        service:
        name: test
        port:
          number: 80
```

	
-OR-

- Configure protection using an existing deployment by running the command:
```
$ kubectl get pod ingress-nginx-2-controller-6dcb748f9-7z6bz -n ingress-nginx-2 -o json | jq .metadata.annotations
{
  "kubernetes.io/psp": "eks.privileged"
}
$ kubectl annotate pod <ingress_pod_id> -n <namespace> vpg=<vpg_id>
pod/ingress-nginx-2-controller-6dcb748f9-7z6bz annotated
```	

#### Protecting Ingress Controller Resources

To display Ingress controller annotation run the following command:
```	
$ kubectl get pod <ingress_pod_id> -n <namespace> -o json | jq .metadata.annotations
{
  "kubernetes.io/psp": "eks.privileged",
  "vpg": "website-vpg1"
}
```	
*Example output for checking VPG configuration with Ingress controller protected*
```
$ kubectl get vpg -n <namespace>
  NAME         STATE      SYNC   SOURCE TARGET STATEFULSETS DEPLOYMENTS SERVICES CONFIGMAPS SECRETS INGRESSES NUMCP RPO       JOURNALHISTORY JOURNALSIZEMB
  website-vpg1 Protecting        node-1 node-1 0            1           0        0          0       1         10    6 seconds 49 seconds     2
```
