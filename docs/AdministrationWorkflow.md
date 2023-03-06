# Z4K Administration

#### Workflow

After deploying Zerto for Kubernetes, create a VPG, configure one-to-many (optional), tag checkpoints, and then test failover.

1.	Create a VPG
2.	Update Existing VPGs
3.	Configure One-to-Many
4.	Tag a Checkpoint
5.	Test Failover

Then, you can perform one of the following:

-	Perform a Failover
-	Restore a Single VPG
-	Perform a Move operation
-	Configure Extended Journal Copy in Kubernetes Environments</br>
	Z4K supports backing up Kubernetes workloads and their data to an Extended Journal Copy and restoring them from the Extended Journal Copy to the original site, or to a different site/namespace.
-	Protect Ingress Controller Resources</br>
	Z4K supports replicating Ingress Controller Resources so networking configuration can be replicated and easily deployed on the recovery site.



#### Protecting Ingress Controller Resources

There are 2 options to configure Ingress Controller Resources with a deployment for protection:
	
-	Configure protection when creating a new deployment, as illustrated in the YAML example below:

	``` yaml
	--- 
	apiVersion: networking.k8s.io/v1
	kind: Ingress
	metadata: 
	  annotations: 
	    nginx.ingress.kubernetes.io/rewrite-target: /
	    vpg: website-vpg1
	  name: minimal-ingress
	spec: 
	  ingressClassName: nginx-example
 	 rules: 
 	   - 
 	     http: ~
 	     paths: 
 	       - 
 	         backend: 
 	           name: test
 	           port: 
 	             number: 80
 	           service: ~
 	         path: /testpath
 	         pathType: Prefix

	```

	
-OR-

-	Configure protection using an existing deployment by running the command:
	```
	$ kubectl get pod ingress-nginx-2-controller-6dcb748f9-7z6bz -n ingress-nginx-2 -o json | jq .metadata.annotations
	{
  	"kubernetes.io/psp": "eks.privileged"
	}
	$ kubectl annotate pod <ingress_pod_id> -n <namespace> vpg=<vpg_id>
	pod/ingress-nginx-2-controller-6dcb748f9-7z6bz annotated
	```	

##### Displaying Ingress Controller Resources

To display Ingress controller annotation run the following command:
```	
$ kubectl get pod <ingress_pod_id> -n <namespace> -o json | jq .metadata.annotations
{
  "kubernetes.io/psp": "eks.privileged",
  "vpg": "website-vpg1"
}
```

**Example output for checking VPG configuration with Ingress controller protected**

```
$ kubectl get vpg -n <namespace>
  NAME         STATE      SYNC   SOURCE TARGET STATEFULSETS DEPLOYMENTS SERVICES CONFIGMAPS SECRETS INGRESSES NUMCP RPO       JOURNALHISTORY JOURNALSIZEMB
  website-vpg1 Protecting        node-1 node-1 0            1           0        0          0       1         10    6 seconds 49 seconds     2
```
