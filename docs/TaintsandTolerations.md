# Z4K Taints and Tolerations
	
Z4K supports taints and tolerations configuration for nodes and pods. 

Use the node annotation “zertorole” to set VRA installation behavior.

#### Adding Zertorole Annotation

-	To force VRA installation, add the following annotation on the current node:

```
kubectl annotate node <node-name> zertorole=worker
```
	
-	To skip VRA installation, add the following annotation on the current node:
	
```
kubectl annotate node <node-name> zertorole=master
```

####  Updating Zertorole Annotation

Use --overwrite to update an annotation that already exists.

-	To update the annotation to force VRA installation, on the current node run the command:

```
kubectl annotate node <node-name> --overwrite zertorole=worker
```
	
-	To update the annotation to skip VRA installation, on the current node run the command:
	
```
kubectl annotate node <node-name> --overwrite zertorole=master
```

#### Removing Zertorole Annotation

To remove a zertorole annotation use a minus (-) sign at the end of the annotation:

```
kubectl annotate node <node-name> zertorole-
```

**Notes:**
- Taints and tolerations are not replicated.
- You must predefine taints and tolerations in pods and nodes for VPG protection **before** recovery oeprations take place.	
- Nodes with a taint that does not allow VRA installation ("NoSchedule" effect) cannot have protected deployments.
- For more information on Kubernetes taints and tolerations, see [Taints and Tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)
