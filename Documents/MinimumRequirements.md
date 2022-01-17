# Minimum Requirements

## Communication Requirements
- All Zerto for Kubernetes components communication occurs using HTTPS, over port 443.

## Storage Requirements
-	Zerto for Kubernetes containerized applications also consume storage:
-	Zerto Kubernetes Manager: 3 GB
-	Zerto Kubernetes Manager Proxy: 1 GB
-	Keycloak Database: 2 GB
-	Zerto for Kubernetes supports protection of Persistent Volumes, configured with VolumeBindingMode, of the type WaitForFirstConsumer.
