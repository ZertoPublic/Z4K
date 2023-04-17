# Z4K Installer

Zerto provides a Z4K Installer tool to simplify the Z4K installation process. You can use it to install a complete Z4K site, or a site with ZKM-PX only. It deploys all required components and verifies the installation.

1. Download the z4k-installer.tar file using wget:

'''
wget https://z4k.zerto.com/z4k-installer.tar
'''

2. Extract all files:

'''
tar -xvf z4k-installer.tar
'''

3. Run the tool.
  .
 ./install-z4k.sh (to deploy zkm+zkm-px on current cluster context)
 or
 ./install-zkm-px.sh (to deploy zkm-px only on current cluster context)

You will be asked to provide required parameters, or you can provide them using dedicated flags (Run the tool with
--help to see all possible flags).
