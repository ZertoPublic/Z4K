2.x Version Changes
===================
* 2.4.67 Workaround for a AKS 1.24 default ingress issue
* 2.4.66 The LTR secret can be placed on any cluster not only on target cluster
* 2.4.65 Fix obfuscator
* 2.4.64 VPG settings validator - update error messages
* 2.4.63 Merge z4k-801-deploy-scripts to master
* 2.4.62 Z4K Pre-Deployment Validator - Added storage classes validations
* 2.4.61 Remove RCM locks during uninstall site
* 2.4.60 Merge z4k-801-add-deployment-scripts to master
* 2.4.59 Added Privileged pods validation
* 2.4.58 - Added Helm Manager version validation
* 2.4.57 Validate initial access token
* 2.4.56 Improve CSI tapping mechanism to be CSI agnostic.
* 2.4.55 In case VRA name exceeds 63 characters limit, use hash of the node name instead
* 2.4.54 Fixed error message text when log collection start time or end time are later than current time.
* 2.4.53 Improve CSI tapping mechanism to be CSI agnostic.
* 2.4.52 Fixed script parameters handling
* 2.4.51 Fixed issue of deleting the journalctl file before collecting it.
* 2.4.50 Added tests to VRA log collector
* 2.4.49 Will collect only Kubernetes logs that are within the requested timeframe
* 2.4.48 Added log collection in timeframe logic for VRA logs.
* 2.4.47 Fixed messages for log collection validations.
* 2.4.46 Added logic of collecting ZKM and ZKM-PX logs within provided timeframe
* 2.4.45 Removed convertion of local time to UTC in kubectl-zrt log collection
* 2.4.44 Added validation for time format in kubectl-zrt
* 2.4.43 Fixed log collection timeframes message and logic
* 2.4.42 Z4K-578 get checkpoints from VRA by in chunks
* 2.4.41 Z4K-720 - Updated kubectl-zrt and added timeframe infra for log collection
* 2.4.40 Check if local download successfully completed.
* 2.4.39 Typo upon download completion
* 2.4.38 Added "vra-" prefix to log file
* 2.4.35 Fixed typo and added path validation for local log collection
* 2.4.34 Improved rest client method signature
* 2.4.33 Improved logger reconfigure mechanizm
* 2.4.32 Logs enhancement - local log collection
* 2.4.31 Add missing hosted service initialization
* 2.4.30 Add csi tapping container
* 2.4.29 unix_socket based solution
* 2.4.28 Z4K -  Fixed runtime rendering of logfiles filepath from nlog.config in NLogHelper.cs.<BR>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Z4K is tested and validated on EKS, AKS and OpenShift platforms.</BR>
* 2.4.27 Log Collection - Fixed wrong kubernetes events comparison and filtering.
* 2.4.26 Copy Linux files only if they don't exist on the system
* 2.4.25 Collect CSI pod logs (optional)
* 2.4.24 Introduced automatic log collection for specific customer case for several days (15 days by default) 
* 2.4.23 Allow to upgrade from master to another branch and vice versa
* 2.4.22 Z4K logs enhancement.
* 2.4.21 Copy Linux binaries to csi pod
* 2.4.20 Merge network_zpref_test to master
* 2.4.19 Implement VPG validation task
* 2.4.18 Obfuscate secret/access key in AWS and for secretKey/applicationId in Azure
* 2.4.17 Fixed validation error messages
* 2.4.16 Merged fix_z4k-503 to master
* 2.4.15 Added VPG validator
* 2.4.14 Remove disks from driver before reopen them after recreate
* 2.4.13 Merged pr_mistake_compile_error to master
* 2.4.12 Merged bug_fix_z4k_459_atomic_verbose_log to master
* 2.4.11 Removed "fo-***" namespace/s after stop/rollback FO operations
* 2.4.10 Fixed duplication site name validation (z4k-36)
* 2.4.9 During uninstall zkm-px site info of the removed site should be deleted from Z4K sites list
* 2.4.8 Added memory counters from driver allocations. (Status)
* 2.4.7 Fixed issue 207463 - Null reference exception on mixed volume types in init containers
* 2.4.6 Checked volume mode is block in pod init containers spec when the volume not found in pod containers
* 2.4.5 Fixed secret obfuscates class to support all types of Json values
* 2.4.4 Fixed kubectl apply issue
* 2.4.3 Obfuscate secret/access keys
* 2.4.2 Added VPG additional validations
* 2.4.1 Fixed issue 205134 - Change the seq to atomic
*2.4.0 Support HPE New CSI
--------------------------
*2.1.0 Implement One-To-Many VPG Configuration
----------------------------------------------
