# Z4K Administration

#### Workflow

After deploying Zerto for Kubernetes, create a VPG, configure one-to-many (optional), tag checkpoints, and then test failover.

1.	Create a VPG
2.	Update Existing VPGs
3.	Configure One-to-Many
4.	Tag a Checkpoint
5.	Test Failover

Then, you can perform one of the following:

-	Perform a Failover
-	Restore a Single VPG
-	Move operation
-	Configure Extended Journal Copy in Kubernetes Environments
	>	Z4K supports backing up Kubernetes workloads and their data to an Extended Journal Copy and restoring them from the Extended Journal Copy to the original site, or to a different site/namespace.
-	Protect Ingress Controller Resources
	>	Z4K supports replicating Ingress Controller Resources so networking configuration can be replicated and easily deployed on the recovery site.
-	Taints and Tolerations
	>	Z4K supports taints and tolerations configuration for nodes and pods.
-	Tweaks
	>	How to view and configure tweaks and values.


#### Creating a VPG


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

In case you need to update an existing VPG you need to create a yaml file as you did it for create VPG,
with additional section: "metadata". The "metadata" section should contain the VPG name and the namespace id:

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
  name: <VPG name>
  namespace: <z4k namespace>
```

Update kubernetes command:

``` shell
kubectl apply -f vpg.yaml
```

#### Configuring One-to-Many

Z4K can protect the same entity multiple times. 

The recommended configuration is to replicate no more than 3 VPGs (inbound & outbound). Exceeding this configuration is possible, bearing in mind that performance degradation may appear if POD/Cluster resources are being overutilized.

One-to-Many serves two main goals:
1.	Enables high availability (HA) for protected VPGs.
2.	Enables Continuous Data Protection (CDP) during migration with a local and a remote copy.

To protect the same entity multiple times:

- Add all of the VPG names in the annotation field with a ';' delimiter sign:

``` yaml
--- 
kind: Deployment
metadata: 
  annotations: 
    vpg: "webApp1Self; webApp1Site2; webApp1Site3 /<VPG names as configured in VPG yaml files>"
  labels: 
    app: debian
  name: debian
    * * *
```   

- Create the VPG by running the command:


``` shell
kubectl create -f vpg.yaml
```

#### Viewing VPG Status

To display the VPG status as well as an overview of which entities are protected within the VPG, the VPG’s SLA and it's settings, run the command:


``` shell
kubectl get vpg
```


#### Tagging a Checkpoint

To tag a checkpoint, run the command:

``` shell
kubectl zrt tag [vpg-name] [tag-name]
```

##### Displaying Available Checkpoints

-	To display a list of all available checkpoints for a VPG, including properties like the checkpoint ID, run the command:


``` shell
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

``` shell
kubectl zrt failover-test [vpg-name] [checkpoint-id]
```

>Where [checkpoint ID] can be either an ID, or enter "latest" for the latest checkpoint.

-	To stop the test run, run the command:

``` shell
kubectl zrt stop-test [vpg-name]
```

#### Performing a Failover
	
-	To failover, run the command:

``` shell
kubectl zrt failover-live [vpg-name] [checkpoint-id]
```

>Where [checkpoint-id] can be either an ID, or enter "latest" for the latest checkpoint.

-	To commit the failover, run the command:

``` shell
kubectl zrt commit [vpg-name]
```

<span class="Note">Note: Upon commit operation, the VPG is deleted.</span>
	
-	To rollback the failover, run the command:

``` shell
kubectl zrt rollback [vpg-name]
```
	
#### Restoring a Single VPG

On a single cluster deployment, only the restore and failover test operations are available. Failover is not available on  single cluster deployments.

-	To restore a single VPG, run the command:

``` shell
kubectl zrt restore [vpg-name] [checkpoint-id]
```
	
>Where [checkpoint-id] can be either an ID, or enter latest, for the latest checkpoint.

-	To commit the restore, run the command:


``` shell
kubectl zrt commit-restore [vpg-name]
```

-	To rollback the restore, run the command:


``` shell
kubectl zrt rollback-restore [vpg-name]
```
#### Move Operation

The move operation allows moving the deployments to it's recovery site without preserving them on the protected site.
The move operation consists of 3 possible commands:
1. move - Start move live (test before commit)
2. commit-move - Commit move
3. rollback-move - Rolling back Move test before commit

The following is used for the above move commands:

``` shell
kubectl zrt move [vpg-name] [checkpoint ID]
```
At that point the VPG state will be updated to StartingMove
If a checkpoint is not tagged use the value 'latest'
Once move operation is completed, the VPG status will be updated to MoveBeforeCommit

``` shell
kubectl zrt rollback-move [vpg-name]
```
The VPG will go back into protecting state in it's protected site without being commited to the recovery site.

``` shell
kubectl zrt commit-move [vpg-name]
```
VPG status will be changed to CommittingMove.
Onc completed, the VPG will be commited, deployment will now exist on the recovery site and VPG will be removed from the environment.

#### Extended Journal Copy in Kubernetes Environments

Z4K supports backing up Kubernetes workloads and their data to an Extended Journal Copy and restoring them from the Extended Journal Copy to the original site, or to a different site.

##### Supported Storage Types

Z4K supports two types of Extended Journal Copy storage:

- AWS S3
- Azure Blob Storage
	
To configure Extended Journal Copy for your Kubernetes environment, use the following procedures:

1.	Back up the VPG
2.	Manually trigger a Backup
3.	Schedule Extended Journal Copy Backups
4.	Restore the VPG from an Extended Journal Copy


##### Backing Up a VPG

To backup a VPG to a target Extended Journal Copy, create the VPG and update the VPG yaml file (vpg.yaml) with the Extended Journal Copy type.

Use the following examples as guidelines.
  
*Example vpg.yaml File - Backing Up to AWS S3*
  
``` yaml
--- 
apiVersion: z4k.zerto.com/v1
kind: vpg
spec: 
  BackupSettings: 
    IsCompressionEnabled: true
    RepositoryInformation: 
      AwsBackupRepositoryInformation: 
        Bucket: <BucketName>
        CredentialsSecretReference: 
          Site: 
            Id: "<site id where is secret installed>"                      
          Id: 
            Name: mysecret
            NamespaceId: ~
              NamespaceName: <Secret Namespace>
        Region: <BucketRegion>
      BackupTargetType: AmazonS3
  JournalDiskSizeInGb: 8
  JournalHistoryInHours: 8
  Name: "<VPG Name>"
  RecoveryStorageClass: <RecoveryStorageClass>
  SourceSite: 
    Id: <SourceSite>
  TargetSite: 
    Id: <TargetSite>  
```

*Example vpg.yaml File - Backing Up to Azure Blob Storage*
  
``` yaml
--- 
apiVersion: z4k.zerto.com/v1
kind: vpg
spec: 
  BackupSettings: 
    IsCompressionEnabled: true
    RepositoryInformation: 
      AzureBackupRepositoryInformation: 
        CredentialsSecretReference: 
          Site: 
            Id: "<site id where is secret installed>"                      
          Id: 
            Name: mysecret
            NamespaceId: ~
              NamespaceName: <Secret Namespace>         
        DirectoryId: c659fda3-cf53-43ad-befe-776ee475dcf5
        StorageAccountName: <Storageaccount>
      BackupTargetType: AzureBlob
  Name: <VPG Name>
  RecoveryStorageClass: <RecoveryStorageClass>
  SourceSite: 
    Id: <SourceSite>
  TargetSite: 
    Id: <TargetSite>

```

-	The AWS S3 access key and secret key should be captured as a Kubernetes secret, whose name appears in the vpg.yaml file. In the example above, this is mysecret.
-	The secret must contain a data item for the AccessKey and a data item for the SecretKey, and can be created in any site to which Zerto Kubernetes Manager has access. In the example above, this is site1.
Example vpg.yaml File - Backing Up to Azure Blob Storage


-	The Azure application id and client secret should be captured as a Kubernetes secret, whose name appears in the vpg.yaml file. In the example above, this is mysecret. 
-	The secret must contain a data item for the ApplicationId and a data item for the ClientSecret, and can be created in any site to which Zerto Kubernetes Manager has access. In the example above, this is site1.


##### Manually Trigger a Backup 
	
You must manually trigger a backup to create a retention set.


-	To manually trigger a backup, run the command:

``` shell
kubectl zrt ltr-backup [vpg-name] [checkpoint-id]
```

>	A backup task is triggered. When the task completes successfully, a retention set is created.


-	To access the generated retention set ID (backupset ID), run the command:

``` shell
kubectl get backupset
```

##### Scheduling Extended Journal Copy Backups

To schedule Extended Journal Copy backups, add **SchedulingAndRetentionSettings** to the VPGs **BackupSettings**.

Use the following example as a guideline.

``` yaml
--- 
apiVersion: z4k.zerto.com/v1
kind: vpg
spec: 
  BackupSettings: 
    IsCompressionEnabled: true
    RepositoryInformation: 
      AwsBackupRepositoryInformation: 
        Bucket: <BucketName>
        CredentialsSecretReference: 
          Site: 
            Id: "<site id where is secret installed>"                      
          Id: 
            Name: mysecret
            NamespaceId: ~
              NamespaceName: <Secret Namespace>
        Region: <BucketRegion>
      BackupTargetType: AmazonS3
    SchedulingAndRetentionSettings: 
      PeriodsSettings: 
        - 
          ExpiresAfterUnit: Years
          ExpiresAfterValue: 1
          Method: Full
          PeriodType: Yearly
        - 
          ExpiresAfterUnit: Months
          ExpiresAfterValue: 12
          Method: Full
          PeriodType: Monthly
        - 
          ExpiresAfterUnit: Weeks
          ExpiresAfterValue: 4
          Method: Full
          PeriodType: Weekly
        - 
          ExpiresAfterUnit: Days
          ExpiresAfterValue: 7
          Method: Incremental
          PeriodType: Daily
  JournalDiskSizeInGb: 8
  JournalHistoryInHours: 8
  Name: <VPG Name>
  RecoveryStorageClass: <RecoveryStorageClass>
  SourceSite: 
    Id: <SourceSite>
  TargetSite: 
    Id: <TargetSite>
```

##### Important Considerations for SchedulingAndRetentionSettings

-	There must be at least one Full Method.
-	There can be no more than one Incremental Method.
-	A Full Method cannot be followed by an Incremental Method. In other words, if there is a Full Method, it should be the last in the chain.
-	Zerto Kubernetes Manager schedules backups and expirations as needed.
	
##### Restoring a VPG from Extended Journal Copy

To restore a VPG from Extended Journal Copy, run the command:

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


#### Protecting Ingress Controller Resources

There are 2 options to configure Ingress Controller Resources with a deployment for protection:
	
-	Configure protection when creating a new deployment, as illustrated in the YAML example below:

``` yaml
--- 
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata: 
  annotations: 
    nginx.ingress.kubernetes.io/rewrite-target: /
    vpg: website-vpg1
  name: minimal-ingress
spec: 
  ingressClassName: nginx-example
  rules: 
    - 
      http: ~
      paths: 
        - 
          backend: 
            name: test
            port: 
              number: 80
            service: ~
          path: /testpath
          pathType: Prefix

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
	


#### Tweaks

Z4K allows users to view and customize tweaks for Z4K components using the following commands:

-	To view existing tweaks and values use the command:
```	
$ kubectl zrt get-potential-tweaks
```
**Example**	
```
$ kubectl zrt get-potential-tweaks
NAME                                                  VALUE               DEFAULT             DESCRIPTION
SyncMonitorIntervalInSeconds                          300                 300
EnableZertoAnalyticsTransmitter                       True                True                Enable Zerto Analytics Transmitter
DisableUndoLog                                        False               False
ScratchSizeInGb                                       2                   2
```
-	To set a new value for an existing tweak, use the command:
```	
$ kubectl zrt set-tweak ScratchSizeInGb <value>
```

**Example**
```
$ kubectl zrt set-tweak ScratchSizeInGb 4
ztweak.z4k.zerto.com/ScratchSizeInGb created
```
	
-	To review the tweaks value and confirm settings, use the command:
```
$ kubectl zrt get-potential-tweaks
```
**Example**
```
$ kubectl zrt get-potential-tweaks
NAME                                                  VALUE               DEFAULT             DESCRIPTION
ScratchSizeInGb                                       4                   2
```
