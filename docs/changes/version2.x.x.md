2.x Version Changes
===================
===================
-------------------
*2.1.0 Implement One-To-Many VPG Configuration
----------------------------------------------
*2.4.0 Support HPE New CSI
--------------------------
* 2.4.1 Fix issue 205134 - Change the seq to atomic
* 2.4.2 Add VPG additional validations
* 2.4.3 Obfuscate secret/access keys
* 2.4.4 Fix kubectl apply issue
* 2.4.5 Fix secret obfuscates class to support all types of Json values
* 2.4.6 Check volume mode is block in pod init containers spec when the volume not found in pod containers
* 2.4.7 Fix issue 207463 - Null reference exception on mixed volume types in init containers
* 2.4.8 Add memory counters from driver allocations. (Status)
* 2.4.9 During uninstall zkm-px site info of the removed site should be deleted from Z4K sites list
* 2.4.10 Fix duplication site name validation (z4k-36)
* 2.4.11 Remove "fo-***" namespace/s after stop/rollback FO operations
* 2.4.12 Merge bug_fix_z4k_459_atomic_verbose_log to master
* 2.4.13 Merge pr_mistake_compile_error to master
* 2.4.14 Remove disks from driver before reopen them after recreate
* 2.4.15 Add VPG validator
* 2.4.16 Merge fix_z4k-503 to master
