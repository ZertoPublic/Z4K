# Disaster Recovery

When the Extended Journal Copy runs for a VPG for the first time, all the data is read and written to the full Retention set. Checkpoints are recorded automatically every few seconds in the full Retention set. Each subsequent incremental Retention process incorporates the changes since the previous run, to provide a complete view of the data at that point in time. The incremental copies rely on the existing full Retention set for that VPG.

When you run a Failover Test operation or Failover operation, you specify a checkpoint to which you want to recover the virtual machines. When you select a checkpoint – either the last automatically generated checkpoint, an earlier checkpoint, or a tagged checkpoint – Zerto makes sure that the virtual machines at the remote site are recovered to this specified point-in-time. 



- Tag a checkpoint
- Perform a Test Failover
- Perform a Failover
- Restore a Single VPG
- Perform a Move operation




#### Additing Tagged Checkpoints

In addition to the automatically generated checkpoints, you can add checkpoints manually to ensure application consistency and to identify events that might influence recovery, such as a planned switch-over to a secondary generator. You can recover the machines in a VPG to any checkpoint in the journal, to one added automatically or to one added manually. Thus, recovery is done to a point-in-time when the data integrity of the protected virtual machines is ensured.

When testing a failover or performing a live failover, you can choose the checkpoint as the point to recover to.

To add a tagged checkpoint, run the command:

``` shell
kubectl zrt tag [vpg-name] [tag-name]
```

Where,

| Parameter |	Description |	
| --------- | ----- | 
| vpg-name  | VPG name |
| tag-name  | A name for the checkpoint |


##### Displaying Available Checkpoints

To display a list of all available checkpoints for a VPG, including automatically generated checkpoints and tagged checkpoints, run the command:

``` shell
kubectl get checkpoints --selector="vpg=vpgs;minAge=5m;maxAge=3d"
```

Where,

| Parameter |	Value |	Mandatory Y/N |
| --------- | ----- | ------------- |
| vpg       | VPG name |	Y |
| minAge    | Minutes: m (example: 5m), Hours: h (example: 5h) , Days: d (example: 5d) | N |
| maxAge    | Minutes: m (example: 5m), Hours: h (example: 5h) , Days: d (example: 5d) | N |



#### Testing Recovery



Use the Failover Test operation to test that the virtual machines are correctly replicated at the recovery site during recovery.

-	To start a failover test, run the command:

	``` shell
	kubectl zrt failover-test [vpg-name] [checkpoint-id]
	```

	Where,</br>
	[checkpoint ID] can be either an ID, or enter "latest" for the latest checkpoint.

-	To stop the failover test, run the command:

	``` shell
	kubectl zrt stop-test [vpg-name]
	```

#### Performing a Failover Live

Use the Failover operation following a disaster to recover protected virtual machines to the recovery site.


	
-	To failover, run the command:

	``` shell
	kubectl zrt failover-live [vpg-name] [checkpoint-id]
	```

	Where,</br>
	[checkpoint-id] can be either an ID, or enter "latest" for the latest checkpoint.

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
	
	Where,</br>
	[checkpoint-id] can be either an ID, or enter latest, for the latest checkpoint.

-	To commit the restore, run the command:


	``` shell
	kubectl zrt commit-restore [vpg-name]
	```

-	To rollback the restore, run the command:


	``` shell
	kubectl zrt rollback-restore [vpg-name]
	```

#### Performing Move Operations

There are 3 commands for different move operations:

1. Move
2. Commit-move
3. Rollback-move

##### Move

The move command starts and tests a live move. 

```
kubectl zrt move [vpg-name] [checkpoint ID]
```

Where,</br>
[checkpoint ID] can be either an ID, or enter "latest" for the latest checkpoint.

- After the command is run, the VPG state will be updated to StartingMove.
- When the move operation is complete, the VPG status will be updated to MoveBeforeCommit.

##### Rollback-Move

The commit-move command rolls back the move test before committing.

```
kubectl zrt rollback-move [vpg-name]
```

- The VPG in the protected site will go back into protecting state without being committed to the recovery site.

##### Commit-Move

The commit-move command is used to commit a move test.

```
kubectl zrt commit-move [vpg-name]
```

- The VPG status will be changed to CommittingMove.
- When the operation has completed, the VPG will be committed and the deployment will now exist on the recovery site.
- The VPG will be removed from the environment.
