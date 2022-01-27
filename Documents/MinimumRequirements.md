# Minimum Requirements

## Communication Requirements
- All Zerto for Kubernetes components communication occurs using HTTPS, over port 443.

## Prerequisites
- Helm Package Manager

## Storage Requirements
-	Zerto for Kubernetes containerized applications also consume storage:
-	Zerto Kubernetes Manager: 3 GB
-	Zerto Kubernetes Manager Proxy: 1 GB
-	Keycloak Database: 2 GB
-	A storageClass with VolumeBindingMode of type "WaitForFirstConsumer" is needed for Zerto to work with persistent volumes.
