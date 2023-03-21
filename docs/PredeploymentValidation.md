# Pre-Deployment Validation

Zerto provides a pre-deployment validator to check that the K8S environment meets the mandatory requirements to deploy Zerto Z4K on the cluster.

#### Installing the Pre-Deployment Validator Tool

Fetch the **Z4K pre-deployment validator** from the z4k.zerto.com repository, using the following command: 

``
wget https://z4k.zerto.com/pre_deployment_validator.tar
``

#### Running the Z4K Pre-Deployment Validator

“ on each cluster that is about to be installed with Z4K protection.

The tar package contains the bash script and all the needed yaml files. 

Extract the tar package within one of the pods in the cluster you will install Z4K on. 

Use the following command to extract to local path: 

``
tar -xvf pre_deployment_validator.tar
``

Execute the 4K Pre-Deployment Validator using the following command:

``
bash ./Z4K_pre_deployment_validator.bash
``

The tool runs and displays on the console, and also creates an output file and a log file.

The logfile contains the information on the utility execution and can be used for troubleshooting. The log file is in the format <clusterName><datetime>/logfile.log.

The output file contains execution details and validations outputs. The output file is in the format <clusterName><datetime>/output.txt.

**Example of Console Output**

``
2023-03-19 14:02:42: Running validations on cluster: TomerCluster2
2023-03-19 14:02:42: Validating Helm Package Manager Version...
2023-03-19 14:02:42: Done
2023-03-19 14:02:42: Validating Privileged Pods Creation...
2023-03-19 14:03:25: Done
2023-03-19 14:03:25: Validating Storage Classes Volume Binding Mode...
2023-03-19 14:03:37: Done
2023-03-19 14:03:37: Binding Mode suitable storage classes include: default, managed, managed-csi,
2023-03-19 14:03:37: Binding Mode not suitable storage classes include: azurefile, azurefile-csi, azurefile-csi-premium,
2023-03-19 14:03:37: Validating Storage Classes Volume Mode Block...
2023-03-19 14:06:05: Done
2023-03-19 14:06:05: VolumeMode Block suitable storage classes include: azurefile, azurefile-csi, azurefile-csi-premium,
2023-03-19 14:06:05: VolumeMode Block not suitable storage classes include: ,
2023-03-19 14:06:05: Suitable storage classes with both mods include: default, managed, managed-csi,
2023-03-19 14:06:05: Done
2023-03-19 14:06:05: **********************************
2023-03-19 14:06:05: **********************************
2023-03-19 14:06:05: Helm Manger minimum version validation: PASS
2023-03-19 14:06:05: Privileged pod validation: FAIL Reason: Failed to create pod with securityContext: privileged
2023-03-19 14:06:05: Volume Binding Mode validation: PASS
2023-03-19 14:06:05: Block StorageClass validation: PASS
2023-03-19 14:06:05: Storage Class Compatibility Validation: PASS
2023-03-19 14:06:05: Compatible Storage Classes include: default, managed, managed-csi,
2023-03-19 14:06:05: The K8S environment does not meet the mandatory requirements to deploy Zerto Z4K as a Recovery and/or Production site. Fix the issues and run the validator again.
``
  
If all validations passed successfully, the following summary will display:
``
The K8S environment meets the mandatory requirements to deploy Zerto Z4K as a Recovery and/or Production site. Proceed with Z4K deployment
``

If some validations failed, the following summary will display:
``
The K8S environment does not meet the mandatory requirements to deploy Zerto Z4K as a Recovery and/or Production site. Fix the issues and run the validator again.
``
Further details can be found in the output and log files.