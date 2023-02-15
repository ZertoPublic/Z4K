# Release Updates

#### Version 2.4.x

- Fixed log collection timeframes message and logic.
- Z4K-578: Get checkpoints from VRA in chunks.
- Z4K-720: Updated kubectl-zrt and added timeframe filtering for log collection.
- Enabled verification of successful local download.  
- Fixed typo upon download completion.
- Add "vra-" prefix to log files.
- Fixed typo and added path validation for local log collection.
- Improved REST client method signature.
- Improved logger reconfigure mechanism.
- Added logs enhancement for local log collection.
- Added missing hosted service initialization.
- Added CSI tapping container.
- Added unix_socket based solution.
- Fixed runtime rendering of log files filepath from nlog.config in NLogHelper.cs.
- Z4K has been successfully tested and validated on EKS, AKS and OpenShift platforms only.
- Enabled Get checkpoints from VRA in chunks.
- Z4K-720: Updated kubectl-zrt and added timeframe filtering for log collection.
- Added verification of succcessful local download.
- Fixed typo and added path validation for local log collection.
- Improved REST client method signature.
- Improved logger reconfigure mechanism.
- Enhanced local log collection.
- Added missing hosted service initialization.
- Added CSI tapping container.
- unix_socket based solution.
- Fixed runtime rendering of logfiles filepath from nlog.config in NLogHelper.cs.
- Z4K is tested and validated on EKS, AKS and OpenShift platforms.
- Log Collection: Fixed wrong kubernetes events comparison and filtering.
- Enabled copy Linux files only if they don't exist on the system.
- Enabled collect CSI pod logs (optional).
- Introduced automatic log collection for specific customer case for several days (7 days by default).
- Enabled upgrade from master to another branch and vice versa.
- Z4K logs enhancement.
- Copy Linux binaries to CSI pod.
- Merged network_zpref_test to master.
- Implemented VPG validation task.
- Obfuscated secret/access key in AWS and for secretKey/applicationId in Azure.
- Fixed validation error messages.
- Added VPG validator.
- Removed disks from driver before reopening them after recreating them.
- Removed "fo-***" namespace/s after stop/rollback FO operations.
- Z4K-36: Fixed duplication site name validation.
- During uninstall ZKM-PX site info of the removed site is deleted from Z4K sites list.
- Added memory counters from driver allocations..
- Fixed issue 207463: Null reference exception on mixed volume types in init containers.
- Added verification that the volume mode is blocked in pod init containers spec when the volume is not found in pod containers.
- Fixed secret obfuscates class to support all types of Json values.
- Fixed kubectl apply issue.
- Obfuscated secret/access keys.
- Added VPG additional validations.
- Fixed issue 205134: Change the seq to atomic.
- Added support for HPE new CSI.

#### Version 2.1.x
- Implemented one-to-many VPG configuration.
