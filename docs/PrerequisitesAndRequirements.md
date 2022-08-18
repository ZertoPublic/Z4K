# Prerequisites and Requirements

#### Communication Requirements
- All Zerto for Kubernetes components communication occurs using HTTPS, over port 443.

#### Prerequisites
- Helm Package Manager, minimum version 3.
- A storage class must be specified and set as the default prior to Z4K installation.
- Cluster security policy should allow creation of privileged pods.

#### Storage Requirements
-	Zerto for Kubernetes containerized applications also consume storage:
-	Zerto Kubernetes Manager: 3 GB
-	Zerto Kubernetes Manager Proxy: 1 GB
-	Keycloak Database: 2 GB
-	A storageClass with VolumeBindingMode of type "WaitForFirstConsumer" is needed for Zerto to work with persistent volumes.
-	The environments storage should support volume mode using Block ("VolumeMode: Block").

<span class="Note">Note
1. Zerto recommends that you set the recovery site StorageClass to "WaitForFistCustomer" volume bind mode.
2. Each recovery VRA has specific volumes that must be bound to it.
If using "immediate" volume binding mode, the volume might be created on a different node and once the VRA POD is created, it would have to move to that node.
If the system doesn't allow the PV to move freely between nodes, the VRA POD won't come up.</span>
