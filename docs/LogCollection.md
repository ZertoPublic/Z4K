# Z4K Log Collection

Virtual replication logs can be collected to help Zerto Support resolve problems related to Z4K.

#### Log Size and Storage Requirements

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

##### Log Location
Logs are stored locally on zkm/zkm-px pods /logs. The ad hoc logs are uploaded to Amazon and stored in S3 bucket.

##### Log Configuration

- The log file size (maxArchiveFiles), max number of archived files (archiveAboveSize) and log level (minlevel) can be changed by editing the appropriate config map.
  - For ZKM the config map is **zkm-config**
  - For ZKM-PX the config map is **zkm-px-config**

**Example log configuration file**
```
keepVariablesOnReload="true"
      throwExceptions="true"
      internalLogLevel="Error"
      autoReload="true">

    <!-- enable asp.net core layout renderers -->
    <extensions>
        <add assembly="NLog.Web.AspNetCore"/>
    </extensions>

    <!-- the targets to write to -->
    <targets async="true">
        <target name="logfile" xsi:type="File"
                fileName="${var:logs_base_dir}/logfile.csv"
                archiveFileName="${var:logs_base_dir}/log.{#####}.zip"
                maxArchiveFiles="200"**                 <!-- Editable value -->
                archiveAboveSize="20971520"**           <!-- Editable value -->
                archiveNumbering="Sequence"
                concurrentWrites="true"
                keepFileOpen="false"
                enableArchiveFileCompression="true">

            <layout xsi:type="CSVLayout" Delimiter="Comma">
                <column name="date" layout="${date:universalTime=true:format=yyyy-MM-dd'T'HH\:mm\:ss.fff'Z'}" />
                <column name="level" layout="${uppercase:${level}}"/>
                <column name="thread" layout="${threadid}"/>
                <column name="mdc" layout="${mdc:item=zertothread}"/>
                <column name="logger" layout="${logger}"/>
                <column name="callsite" layout="${callsite:className=false:includeSourcePath=false}"/>
                <column name="message" layout="${message}"/>
                <column name="exception" layout="${exception:format=:format=Type,Method,ToString}"/>
            </layout>
        </target>

        <target xsi:type="Console" name="logconsole"
                layout="${longdate},${level},${threadid},${mdc:item=zertothread},${logger},${callsite:className=false:includeSourcePath=false},${message},${exception:format=Type,Method,ToString}" />
    </targets>

    <!-- rules to map from logger name to target -->
    <rules>
        <!-- Enable JwtBearer token validation logging -->
        <logger name="Microsoft.AspNetCore.Authentication.JwtBearer.JwtBearerHandler" minlevel="Info" final="true" writeTo="logfile" />
        <!--Skip non-critical Microsoft logs and so log only own logs-->
        **<logger name="Microsoft.*" maxlevel="Info" final="true" />**        <!-- Editable value -->
        <!-- BlackHole without writeTo -->
        <logger name="*" minlevel="Debug" writeTo="logconsole,logfile"/>
    </rules>
</nlog>
```

#### Using Remote Log Collection

Remote log collection enables Zerto Support engineers to collect logs from a customer's environment.

Run the following command to collect local logs remotely:

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

#### Collecting Logs to a Local Drive

Run the following command to collect logs to a local file system:

```
collect-logs-locally <pathToFilename.zip> <StartTime> <endTime> 
```

Where:

| Parameter |	Comment |
| --------- | ------- |
| pathToFilename.zip | (Required) Path to log bundle zip file. If you specify a folder that doesn't exist, you will be prompted to create one.| 
| startTime | (Optional) Collection start time in yyyy-mm-dd HH:mm:ss format. Default is 7 days. |
| endTime | (Optional) Collection end time in yyyy-mm-dd HH:mm:ss format. Default is now. |

Example:
```
kubect1 zrt collect-logs-locally "/temp/myNewBundle.zip" 2023-01-22 06:00:00" "2023-01-23 06:00:00"
```

Access the zip file in your local directory, and unzip to review the log files.

#### Collecting Logs using a Script

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

#### Enabling Automatic Log Collection

Automatic log collection, autologging, may be helpful when a customer previously experienced an issue and the archived log files no longer contain the log file because the log cycle already deleted it.

To enable autologging:
- Set tweak **AutoLogCaseNumber** with the customer bug or case number.
- Set tweak **AutoLogForNDays** with the number of days to run autologging. The default is 15 days. 

By default autologging is performed at noon every day. You can change the time value during the helm install/upgrade procedure by providing the "autoLoggingTimeout" cron value:
```
autoLoggingTimeout: "0 0 0 * * *" 
```

Use [Cron Descryptor](https://www.freeformatter.com/cron-expression-generator-quartz.html) to define cron values.      
