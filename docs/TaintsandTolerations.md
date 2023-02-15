# Taints and Tolerations
	
Z4K supports taints and tolerations configuration for nodes and pods.

You can add a node annotation called “zertorole” to force VRA installation behavior.

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

-	To update the annotation to force VRA installation, on the current node run the command:

```
kubectl annotate node <node-name> --overwrite zertorole=worker
```
	
-	To update the annotation to skip VRA installation, on the current node run the command:
	
```
kubectl annotate node <node-name> --overwrite zertorole=master
```

<span class="Note">Note: Use --overwrite to update an annotation that already exists.</span>


#### Removing Zertorole Annotation

To remove a zertorole annotation use a minus - sign at the end of the annotation:

```
kubectl annotate node <node-name> zertorole-
```

<span class="Note">Notes:
-	Nodes that are tainted with a taint that does not allow VRA installation ("NoSchedule" effect) cannot have protected deployments.
-	Taints and tolerations are not replicated.
-	When Taints and Tolerations are in use they must be predefined in pods and nodes for VPG protection, **before** recovery oeprations take place.</span>	

-	For more info, see [Taints and Tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)
