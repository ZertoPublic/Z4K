# Z4K Installer

Zerto provides a Z4K Installer tool to simplify the Z4K installation process. You can use it to install a complete Z4K site with Zerto Kubernetes Manager (ZKM) and Zerto Kubernetes Manager Proxy (ZKM-PX), or a site with ZKM-PX only. It deploys all required components and verifies the installation.

1. Download the z4k-installer.tar file using wget:

  ```
  wget https://z4k.zerto.com/z4k-installer.tar
  ```

2. Extract all files:

  ```
  tar -xvf z4k-installer.tar
  ```

3. Run the tool.
  
  - To deploy ZKM and ZKM-PX on the current cluster, run:
 
    ```
    ./install-z4k.sh
    ```
   
   - To deploy only ZKM-PX on the current cluster, run:
   
   ```
   ./install-zkm-px.sh 
   ```

  You will be asked to provide required parameters, or you can provide them using dedicated flags by running the tool with --help to see all possible flags.
  For example:
  
   ```
   ./install-z4k.sh --help
   ```
 
