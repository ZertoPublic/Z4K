# Extended Journal Copy

Z4K supports backing up Kubernetes workloads and their data to an Extended Journal Copy and restoring them from the Extended Journal Copy to the original site, or to a different site.

#### Supported Storage Types

Z4K supports two types of Extended Journal Copy storage:

- AWS S3
- Azure Blob Storage
	
To configure an Extended Journal Copy for your Kubernetes environment, use the following procedures:

1.	Back up the VPG.
2.	Manually trigger a Backup.
3.	Schedule Extended Journal Copy Backups.
4.	Restore the VPG from an Extended Journal Copy.

#### Backing Up a VPG to a Target Extended Journal Copy

To backup a VPG to a target Extended Journal Copy, create the VPG and update the VPG yaml file (vpg.yaml) with the Extended Journal Copy type.

Use the following examples as guidelines.

##### Example vpg.yaml File for Backing Up to AWS S3
  
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
            NamespaceId:
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

-	The AWS S3 access key and secret key should be captured as a Kubernetes secret, whose name appears in the vpg.yaml file. In the example above, this is *mysecret*.
-	The secret must have a yaml file that contains a data item for the AccessKey and a data item for the SecretKey. The secret yaml file can be created in any site to which Zerto Kubernetes Manager has access. 

	**Example Secret Yaml File for AWS S3**
	```
	apiVersion: v1
	kind: Secret
	metadata:
	  name: <Secret Name>
	  namespace: <Secret Namespace>
	type: Opaque
	data:
	  AccessKey: <access key>
	  SecretKey: <secret key>
	```


##### Example vpg.yaml File for Backing Up to Azure Blob Storage
  
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
            NamespaceId:
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

-	The Azure application id and client secret should be captured as a Kubernetes secret, whose name appears in the vpg.yaml file. In the example above, this is *mysecret*. 
-	The secret must have a yaml file that contains a data item for the ApplicationId and a data item for the ClientSecret. The yaml file can be created in any site to which Zerto Kubernetes Manager has access.

	**Example Secret Yaml File for Azure Blob Storage**
	
	```
	apiVersion: v1
	kind: Secret
	metadata:
	  name: <Secret Name>
	  namespace: <Secret Namespace>
	type: Opaque
	data:
	  ApplicationId: <application ID>
	  ClientSecret: <client secret>
	```

#### Manually Trigger a Backup 
	
You must manually trigger a backup to create a retention set.


-	To manually trigger a backup, run the command:

	``` shell
	kubectl zrt ltr-backup [vpg-name] [checkpoint-id]
	```

	A backup task is triggered. When the task completes successfully, a retention set is created.


-	To access the generated retention set ID (backupset ID), run the command:

	``` shell
	kubectl get backupset
	```

#### Scheduling Extended Journal Copy Backups

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

#### Important Considerations for SchedulingAndRetentionSettings

-	There must be at least one Full Method.
-	There can be no more than one Incremental Method.
-	A Full Method cannot be followed by an Incremental Method. In other words, if there is a Full Method, it should be the last in the chain.
-	Zerto Kubernetes Manager schedules backups and expirations as needed.


#### Restoring a VPG from Extended Journal Copy

To restore a VPG from Extended Journal Copy, run the command:

```
kubectl zrt ltr-restore [backupset-id] [site-id] [storage-class] [namespace]
```

Where,

| Parameter |	Comment |
| --------- | ------- |
| site-id | Identifier of the site to which you want to restore. |
| storage-class | Storage class, with which persistent volumes for the restored data is created. |
| namespace | namespace in which you want the restored Kubernetes entities to be created. |

These parameters give you flexibility in restoring a VPG to the original site, or to a different site or namespace.
You can also restore from a repository that has VPGs backupsets from a different site and restore them to a new site using the parameter backupset-id.
	
When the restore task completes successfully, Kubernetes entities with the prefix "res-" are created in the specified site and namespace.
