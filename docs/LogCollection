# Log Collection and Retention

Zerto for Kubernetes uses Apache log4net™ logging framework to generate, collect and output log statements.

##### Log Volume Size
- A ZKM service can have up to 200 log files.
- A ZKM-PX service can have up to 200 log files.

##### Log Rotation
- Log files are automatically archived when the log file size exceeds 10MB. 
- Archived log files can be deleted manually.

##### Required Storage
- A log file is 1.8MB after automatic archiving.
Therefore:
- A ZKM service needs 200 x 1.8MB = ~360MB
- A ZKM-PX service needs 200 x 1.8MB = ~360MB
- All log configuration such as log file size, log level (debug,info e.t.c), max number of archived files can be changed by editing the appropriate config map.
For ZKM - zkm-config
For ZKM-PX - zkm-px-config

##### Log Location
Logs are stored locally on zkm/zkm-px pods /logs. The ad hoc logs are uploaded to Amazon and stored in S3 bucket.


#### Collect Logs to S3

Run the following command to collect local logs to S3:

```
kubectl-zrt collect-logs <caseNum> <StartTime> <endTime>
```

Where:

| Parameter |	Comment |
| --------- | ------- |
| caseNum | (Required) Case name or description.| 
| startTime | (Optional) Collection start time in yyyy-mm-dd HH:mm:ss format. Default is 7 days. |
| endTime | (Optional) Collection end time in yyyy-mm-dd HH:mm:ss format. Default is now. |

Example:
```
kubectl-zrt collect-logs <case/bug number>
kubect1 zrt collect-logs "case12345" 2023-01-22 06:00:00" "2023-01-23 06:00:00"
```

#### Collect Logs Locally

Collect logs to a local file system by running the command:

```
collect-logs-locally <caseNum> <StartTime> <endTime></tmp/tmp/filename.zip 
```

Where:

| Parameter |	Comment |
| --------- | ------- |
| caseNum | (Required) Case name or description.| 
| startTime | (Optional) Collection start time in yyyy-mm-dd HH:mm:ss format. Default is 7 days. |
| endTime | (Optional) Collection end time in yyyy-mm-dd HH:mm:ss format. Default is now. |

Example:
```
kubect1 zrt collect-logs-locally "/temp/myNewBundle.zip" 2023-01-22 06:00:00" "2023-01-23 06:00:00"
```

#### Collect Logs by Running a Script

Follow these steps to run a script on the ZKM-PX in the background to collect logs to S3:

-	Connect to the pod using the command:
```
kubect1 exec
```

-	Run one of the following scripts:

```
/scripts/collect_logs_lt.bash
```

-OR-

```
/scripts/collect_logs_ng.bash
```

#### Automatic Log collection

Automatic log collection, autologging,  may be helpful when a customer experienced an issue in the past and the archived log files not longer contain the log file because the log cycle already deleted it.

To enable autologging:
- Set tweak **AutoLogCaseNumber** with the customer bug or case number.
- Set tweak **AutoLogForNDays** with the number of days to run autologging. The default is 15 days. 

By default autologging is performed at noon every day. You can change the time value during the helm install/upgrade procedure by providing the "autoLoggingTimeout" cron value:
```
autoLoggingTimeout: "0 0 0 * * *" 
```

Use [Cron Descryptor](https://www.freeformatter.com/cron-expression-generator-quartz.html) to define cron values.      
