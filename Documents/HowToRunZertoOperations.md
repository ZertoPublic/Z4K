# How To Run Zerto Operations

After deploying Zerto for Kubernetes, create a VPG, tag checkpoints then test failover:

1.	[Creating a VPG](#creating-a-vpg)
2.	[Tagging a Checkpoint](#tagging-a-checkpoint)
3.	[Testing Failover](#testing-failover)

Then, when you need to, perform one of the following:

-	[Performing a Failover](#performing-a-failover)
-	[Restoring a Single VPG](#restoring-a-single-vpg)

Zerto for Kubernetes supports backing up Kubernetes workloads and their data to a Long-term Repository and restoring them from the Long-term Repository to the original site, or to a different site/namespace.

-	[Long-term Retention (LTR) in Kubernetes Environments](#long-term-retention-ltr-in-kubernetes-environments)

Log collection occurs automatically, and the logs are uploaded to Amazon S3. You can also collect logs ad hoc.

- [Log Collection](#log-collection)

## Creating a VPG

To create a VPG:

1.	Create a .yaml file to represent a VPG.
In the below example the VPG webApp1:

-	Is configured to self replicate to its source cluster.
-	Will use the storage class goldSC.
-	SLA is 12 hours of history.
-	The Journal can expand up to 160 GB to meet the history requirement.

> Note:	It is not mandatory to configure the Journal disk size (JournalDiskSizeInGb) and history (JournalHistoryInHours); they have default values of 2 GB and 8 hours respectively.

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

2.	Annotate Kubernetes entities to include them in the VPG.

-	A VPG can contain a selection of entities like stateful sets, deployments, services, secrets and configmaps.
-	Applications consisting of several components with inter-dependencies (for example secrets and deployments), should all be tagged with the same VPG annotation in order for the Failover operation to succeed.
-	To include an entity to a VPG, you need to annotate it with the VPG name.

See the following example of deployment protection:

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

3.	Create the VPG by running the following command:

```
kubectl create -f vpg.yaml
```

4.	To get the VPG status, run the following command:

```
kubectl get vpg
```

By running this command, you can also see an overview of which entities are protected within the VPG, the VPG’s SLA and it's settings.

## Tagging a Checkpoint

To view available checkpoints:

•	Run the following command.
This will present the user with a list of all available checkpoints for the VPG, including properties like the checkpoint ID.

```
kubectl get checkpoints --selector="vpg=vpgs;minAge=5m;maxAge=3d"
```

Where:

| Parameter |	Value |	Mandatory Y/N |
| --------- | ----- | ------------- |
| vpg       |	VPG name |	Y |
| minAge    | Minutes: m (example: 5m), Hours: h (example: 5h) , Days: d (example: 5d) | N |
| maxAge    | Minutes: m (example: 5m), Hours: h (example: 5h) , Days: d (example: 5d) | N |

To tag a checkpoint:

•	Run the following command:

```
kubectl zrt tag <VPG Name> <tag name>
```

## Testing Failover

Run the following command to test failover.

To test failover:

-	Run the following command, where <checkpoint ID> can be either an ID, or enter latest, for the latest checkpoint.

```
kubectl zrt failover-test <vpg name> <checkpoint ID>
```

To stop the test run:

•	Run the following command:

```
kubectl zrt stop-test <vpg name>
```

## Performing a Failover

Run the following command to failover.

To failover:

- Run the following command, where <checkpoint ID> can be either an ID, or enter latest, for the latest checkpoint.

```
kubectl zrt failover-live <vpg name> <checkpoint ID>
```

To commit the failover:

-	Run the following command:

```
kubectl zrt commit <vpg name>
```

To rollback the failover:

- Run the following command:

```
kubectl zrt rollback <vpg name>
```

## Restoring a Single VPG

On a single cluster deployment, only the restore and failover test operations are available. Failover is not available.

To restore a single VPG:

-	Run the following command, where <checkpoint ID> can be either an ID, or enter latest, for the latest checkpoint.

```
kubectl zrt restore <vpg name> <checkpoint ID>
```

To commit the restore:

-	Run the following command:

```
kubectl zrt commit-restore <vpg name>
```

To rollback the restore:

-Run the following command:

```
kubectl zrt rollback-restore <vpg name>
```

## Long-term Retention (LTR) in Kubernetes Environments

Zerto for Kubernetes supports backing up Kubernetes workloads and their data to a long-term repository and restoring them from the long-term repository to the original site, or to a different site. The repository where backed up data is kept is called a Long-term Retention (LTR) repository.

### Supported Repository Types
Zerto for Kubernetes supports two LTR repository types:

- AWS S3
- Azure Blob Storage
	
To configure Long-term Retention for your Kubernetes environment, use the following procedures:

1.	Backing up a VPG
2.	Manually Trigger a Backup
3.	Scheduling Long-term Retention Backups
4.	Restoring a VPG from a Long-term Repository


### Backing up a VPG

To backup a VPG to a target LTR repository, you first need to create the VPG and update the VPG yaml file (vpg.yaml) with the LTR repository type.

Use the following examples as guidelines.
Then, continue to Manually Trigger a Backup
  
Example vpg.yaml File - Backing Up to AWS S3
  
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

Example vpg.yaml File - Backing Up to Azure Blob Storage
  
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


-	The Azure application id and client secret should be captured as a Kubernetes secret, whose name appears in the vpg.yaml file. In the example above, this is mysecret. In the example above, this is mysecret.
-	The secret must contain a data item for the ApplicationId and a data item for the ClientSecret, and can be created in any site to which Zerto Kubernetes Manager has access. In the example above, this is site1.
Manually Trigger a Backup
After you created the VPG and updated the VPG yaml file (vpg.yaml) with the LTR repository type, you can manually trigger a backup. This creates a retention set.

To do this, run the following command:

```
kubectl zrt ltr-backup <vpg-name> <checkpoint-id>
```

A backup task is triggered.

When the task completes successfully, a retention set is created.

You can access the generated retention set ID (backupset id) by running the following command:

```
kubectl get backupset
```

### Scheduling Long-term Retention Backups

To schedule Long-term Retention backups, add SchedulingAndRetentionSettings to the vpgs BackupSettings.

Use the following example as guideline.

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


SchedulingAndRetentionSettings considerations:

-	There must be at least one Full Method.
-	There can be no more than one Incremental Method.
-	A Full Method cannot be followed by an Incremental Method.
In other words, if there is a Full Method, it should be the last in the chain.

-	Zerto Kubernetes Manager schedules backups and expirations as needed.
Restoring a VPG from a Long-term Repository
To restore a VPG from a Long-term repository, run the following command:

```
kubectl zrt ltr-restore <backupset-id> <site-id> <storage-class> <namespace>
```

A restore task is triggered.

Consider the following, taking into account that these parameters give you flexibility in restoring to the original site, or to a different site or namespace.

| Parameter |	Comment |
| --------- | ------- |
| site-id | Identifier of the site to which you want to restore. |
| storage-class | Storage class, with which persistent volumes for the restored data is created. |
| namespace | namespace in which you want the restored Kubernetes entities to be created. |

When the restore task completes successfully, Kubernetes entities with the prefix res- are created in the specified site and namespace.

## Log Collection

Zerto for Kubernetes logs are collected by the system and automatically uploaded to Amazon S3.

Log location: S3 bucket

Ad Hoc Log Collection
Use one of the following methods:

-	Running a script on Zerto Kubernetes Manager Proxy (ZKM-PX)

Run the following command, which runs the script in the background:

```
kubectl-zrt collect-logs <case/bug number>
```

- Or, you could do the following:

1.	Connect to the pod using the following command: 

```
kubectl exec
```
  
2.	Run the following script: 

```
/scripts/collect_logs_lt.bash
```

-	Running a script on Zerto Kubernetes Manager (ZKM)
  
1.	Connect to the pod using the following command: 

```
kubectl exec
```
  
2.	Run the following script: 

```
/scripts/collect_logs_ng.bash
```
