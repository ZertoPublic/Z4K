# Tweaks

Z4K allows users to view and customize tweaks for Z4K components.

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
