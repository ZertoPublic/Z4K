# Administration Guide

After deploying Zerto for Kubernetes, create a VPG, configure one-to-many (optional), tag checkpoints, and then test failover:

1.	[Create a VPG](#Creating-a-VPG)
2.	[Configure One-to-Many](#Configuring-One-to-Many)
3.	[Tag a Checkpoint](#Tagging-a-Checkpoint)
4.	[Test Failover](#Testing-Failover)

Then, you can perform one of the following:

-	[Perform a Failover](#Performing-a-Failover)
-	[Restore a Single VPG](#Restoring-a-Single-VPG)
-	[Configure Long-term Retention (LTR) in Kubernetes Environments](#Long-Term-Retention-in-Kubernetes-Environments)
	>	Zerto for Kubernetes supports backing up Kubernetes workloads and their data to a Long-term Repository and restoring them from the Long-term Repository to the original site, or to a different site/namespace.
- [Log Retention](#Log-Retention)
	>	Log collection occurs automatically, and the logs are uploaded to Amazon S3. You can also collect logs ad hoc.
-	[Protect Ingress Controller Resources](#Protecting-Ingress-Controller-Resources)
	>	Zerto for Kubernetes supports replicating Ingress Controller Resources so networking configuration can be replicated and easily deployed on the recovery site.
-	[Taints and Tolerations](#Taints-and-Tolerations)
	>	Z4K supports taints and tolerations configuration for nodes and pods.
-	[Tweaks](#Tweaks)
	>	How to view and configure tweaks and values.


### Creating a VPG


1. Create a .yaml file to represent a VPG.
    > In the following example the VPG webApp1:
    >>-	Is configured to self replicate to its source cluster.
    >>-	Will use the storage class goldSC.
    >>-	SLA is 12 hours of history.
    >>-	The Journal can expand up to 160 GB to meet the history requirement.

<span class="Note">Note: It is not mandatory to configure the Journal disk size (JournalDiskSizeInGb) and history (JournalHistoryInHours); they have default values of 2 GB and 8 hours respectively.</span>





    ```
    apiVersion: z4k.zerto.com/v1
    kind: vpg
    spec:
      Name : “webApp1”
      SourceCluster :
        Id: "prod_cluster”
       TargetCluster :
        Id: "prod_cluster"
      RecoveryStorageClass : GoldSC
      JournalDiskSizeInGb : 160
      JournalHistoryInHours : 12
     ```
     
2. Annotate Kubernetes entities to include them in the VPG.

>>-	A VPG can contain a selection of entities like stateful sets, deployments, services, secrets and configmaps.

>>-	Applications consisting of several components with inter-dependencies (for example secrets and deployments), should all be tagged with the same VPG annotation in order for the Failover operation to succeed.

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

### Configuring One-to-Many

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

#### Viewing VPG Status

To display the VPG status as well as an overview of which entities are protected within the VPG, the VPG’s SLA and it's settings, run the command:


```
kubectl get vpg
```


### Tagging a Checkpoint

To tag a checkpoint, run the command:

```
kubectl zrt tag [vpg-name] [tag-name]
```

#### Displaying Available Checkpoints

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


### Testing Failover

-	To test failover, run the command:

```
kubectl zrt failover-test [vpg-name] [checkpoint-id]
```

>Where [checkpoint ID] can be either an ID, or enter "latest" for the latest checkpoint.

-	To stop the test run, run the command:

```
kubectl zrt stop-test [vpg-name]
```

### Performing a Failover
	
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
	
### Restoring a Single VPG

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


### Long Term Retention in Kubernetes Environments

Zerto for Kubernetes supports backing up Kubernetes workloads and their data to a long-term repository and restoring them from the long-term repository to the original site, or to a different site. The repository where backed up data is kept is called a Long-term Retention (LTR) repository.

#### Supported Repository Types

Zerto for Kubernetes supports two LTR repository types:

- AWS S3
- Azure Blob Storage
	
To configure Long-term Retention for your Kubernetes environment, use the following procedures:

1.	[Back up the VPG](#Backing-up-a-VPG)
2.	[Manually trigger a Backup](#Manually-Trigger-a-Backup)
3.	[Schedule Long-term Retention Backups](#Scheduling-Long-Term-Retention-Backups)
4.	[Restore the VPG from a Long-term Repository](#Restoring-a-VPG-from-a-Long-Term-Repository)



#### Backing up a VPG

To backup a VPG to a target LTR repository, create the VPG and update the VPG yaml file (vpg.yaml) with the LTR repository type.

Use the following examples as guidelines.
  
*Example vpg.yaml File - Backing Up to AWS S3*
  
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

*Example vpg.yaml File - Backing Up to Azure Blob Storage*
  
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

-	The AWS S3 access key and secret key should be captured as a Kubernetes secret, whose name appears in the vpg.yaml file. In the example above, this is mysecret.
-	The secret must contain a data item for the AccessKey and a data item for the SecretKey, and can be created in any site to which Zerto Kubernetes Manager has access. In the example above, this is site1.
Example vpg.yaml File - Backing Up to Azure Blob Storage


-	The Azure application id and client secret should be captured as a Kubernetes secret, whose name appears in the vpg.yaml file. In the example above, this is mysecret. 
-	The secret must contain a data item for the ApplicationId and a data item for the ClientSecret, and can be created in any site to which Zerto Kubernetes Manager has access. In the example above, this is site1.


#### Manually Trigger a Backup 
	
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

#### Scheduling Long Term Retention Backups

To schedule Long-term Retention backups, add **SchedulingAndRetentionSettings** to the VPGs **BackupSettings**.

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

##### Important Considerations for SchedulingAndRetentionSettings

-	There must be at least one Full Method.
-	There can be no more than one Incremental Method.
-	A Full Method cannot be followed by an Incremental Method. In other words, if there is a Full Method, it should be the last in the chain.
-	Zerto Kubernetes Manager schedules backups and expirations as needed.
	
#### Restoring a VPG from a Long Term Repository

To restore a VPG from a Long-term repository, run the command:

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
You can also restore from a repository that has VPGs backupsets from a different site and restore them to a new site using the parameter backupset-id.
	
When the restore task completes successfully, Kubernetes entities with the prefix "res-" are created in the specified site and namespace.


### Log Retention

Zerto for Kubernetes uses Apache log4net™ logging framework to generate, collect and output log statements.

##### Log Volume Size
- A ZKM service can have up to 200 log files.
- A ZKM-PX service can have up to 50 log files.

##### Log Rotation
- Log files are automatically archived when the log file size exceeds 10MB. 
- Archived log files can be deleted manually.

##### Required Storage
- A log file is 0.6MB after automatic archiving.

Therefore:
- A ZKM service needs 200 x 0.6MB = ~120MB
- A ZKM-PX service needs 50 x 0.5MB = ~30MB

##### Log Location
Logs are stored locally on zkm/zkm-px pods /logs. After ad hoc log collection logs are uploaded to Amazon and stored in S3 bucket.

#### Ad Hoc Log Collection

Use one of the following methods to generate logs.

##### Ad Hoc Log Collection Method 1
Run the following command, which runs a script on Zerto Kubernetes Manager Proxy (ZKM-PX) in the background:

```
kubectl-zrt collect-logs <case/bug number>
```

##### Ad Hoc Log Collection Method 2

-	Connect to the pod using the command: 

```
kubectl exec
```
  
-	Run one of the following scripts: 

```
/scripts/collect_logs_lt.bash
```
*-OR-*
```
/scripts/collect_logs_ng.bash
```

### Protecting Ingress Controller Resources

There are 2 options to configure Ingress Controller Resources with a deployment for protection:
	
-	Configure protection when creating a new deployment, as illustrated in the YAML example below:

```
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

	
*-OR-*

-	Configure protection using an existing deployment by running the command:
```
$ kubectl get pod ingress-nginx-2-controller-6dcb748f9-7z6bz -n ingress-nginx-2 -o json | jq .metadata.annotations
{
  "kubernetes.io/psp": "eks.privileged"
}
$ kubectl annotate pod <ingress_pod_id> -n <namespace> vpg=<vpg_id>
pod/ingress-nginx-2-controller-6dcb748f9-7z6bz annotated
```	

### Protecting Ingress Controller Resources

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
	
### Taints and Tolerations
	
Z4K supports taints and tolerations configuration for nodes and pods.

<span class="Note">Note: Nodes that are tainted with a taint that does not allow VRA installation cannot have it's deployments protected.</span>
	
-	Taints and tolerations are not replicated.
-	When Taints and Tolerations are in use they need to be predefined in pods and nodes for VPG protection, before recovery oeprations take place.
-	For more info on Taints and Tolerations see [Taints and Tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)

### Tweaks

Z4K allows users to view and customize tweaks for Z4K components using the following commands:

To view existing tweaks and values:
```
$ kubectl zrt get-potential-tweaks
NAME                                                  VALUE               DEFAULT             DESCRIPTION
SyncMonitorIntervalInSeconds                          300                 300
EnableZertoAnalyticsTransmitter                       True                True                Enable Zerto Analytics Transmitter
DisableUndoLog                                        False               False
ScratchSizeInGb                                       2                   2
```
To set a new value for an existing tweak:
```
$ kubectl zrt set-tweak ScratchSizeInGb 4
ztweak.z4k.zerto.com/ScratchSizeInGb created
```
	
After the change in value you can review the tweaks value to confirm the change:
```
$ kubectl zrt get-potential-tweaks
NAME                                                  VALUE               DEFAULT             DESCRIPTION
ScratchSizeInGb                                       4                   2
```


