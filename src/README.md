#Deploying and Running a web app using Kubernetes and docker
==================
In this project we deployed a web application on **[Kubernetes](http://kubernetes.io)** using Docker containers on CoreOS. 
The deployed Kubernetes cluster includes 1 CoreOS master VM and 2 slave VMs.

##Basic Requirements: 
 - **[VirtualBox](https://www.virtualbox.org/wiki/Linux_Downloads)** and 
 - **[Vagrant](https://www.vagrantup.com/downloads.html)** - Refer to **[this guide](https://coreos.com/kubernetes/docs/latest/kubernetes-on-vagrant.html)** for learning how to install vagrant.

##Approaches:

Run the Vagrantfile by following command:
~~~ sh
vagrant up
~~~
With the previous the CoreOS instances will be created. You can run the VirtualBox GUI to see that the instances are running, or type in
~~~ sh
vagrant status
~~~
to see the status of the VMs.

Now ssh to CoreOS 'master' instance by following command:
~~~ sh
vagrant ssh master
~~~
**NOTE:**
- If proxy has to be set then set https_proxy, http_proxy and no_proxy in every terminal).
- Also, when working behind a proxy, write: sudo HTTP_PROXY=username@proxy:8080 [command], instead of sudo [command] for all 
  Docker or Kubernetes commands. 

####Method 1 (Docker)
In the CoreOS terminal, 
~~~ sh
sudo docker run -d -P udyank/studentdbapp
~~~
This command will return a [container_code], which we will use as:
~~~ sh
docker port [container_code] 
~~~ 
This will give us a mapping from virtual TCP port to actual IP and port (Default: localhost:32768). <br/>
You have to do "ifconfig" to see the public ip of master's localhost (Default: 172.17.8.101). <br/>
Now go to this IP (172.17.8.101:32768) to view the app. And we're done!! <br/>
If we do the above on both node-01 and node-02 also, we can access the app from all three IPs. <br/>



####Method 2 (Kubernetes)
In the CoreOS terminal, run the following commands in sequence: 
~~~ sh
sudo mkdir -p /opt/kubernetes/bin 
sudo chown -R core: /opt/kubernetes
cd /opt/kubernetes
wget https://github.com/kelseyhightower/kubernetes-coreos/releases/download/v0.0.1/kubernetes-coreos.tar.gz
tar -C bin/ -xvf kubernetes-coreos.tar.gz
~~~
Start etcd service by 
~~~ sh
sudo systemctl start etcd
~~~
Start Docker service by 
~~~ sh
sudo docker -d
~~~
Open new terminal of CoreOS master and start kubernetes' apiserver by 
~~~ sh
sudo /opt/kubernetes/bin/apiserver --address=127.0.0.1 --port=8080 --etcd_servers=http://127.0.0.1:4001 --machines=127.0.0.1 --logtostderr=true
~~~
Open new terminal of CoreOS master and start kubernetes' controller-manager by 
~~~ sh
sudo /opt/kubernetes/bin/controller-manager --master=127.0.0.1:8080 --etcd_servers=http://127.0.0.1:4001 --logtostderr=true
~~~
Open new terminal of CoreOS master and start kubelet by 
~~~ sh 
sudo /opt/kubernetes/bin/kubelet --address=127.0.0.1 --port=10250 --hostname_override=127.0.0.1 --etcd_servers=http://127.0.0.1:4001 --logtostderr=true
~~~
Open new terminal of CoreOS master and start proxy by 
~~~ sh
sudo /opt/kubernetes/bin/proxy --etcd_servers=http://127.0.0.1:4001 -logtostderr=true
~~~

Open new terminal of CoreOS master and run kubernetes commands using kubecfg as shown below.
To deploy and run a web app use following command
~~~ sh
sudo /opt/kubernetes/bin/kubecfg -h http://127.0.0.1:8080 -c web.json create /pods
~~~
The file web.json has image details and content of file is 
~~~ sh
{
      "id": "web",
      "desiredState": {
        "manifest": {
          "version": "v1beta1",
          "id": "web",
          "containers": [{
        "name": "web",
        "image": "udyank/studentdbapp",
        "ports": [{
          "containerPort": 80,
          "hostPort": 80
        }]
          }]
        }
      },
      "labels": {
        "name": "web"
      }
}

~~~

To see list of pods use following command 
~~~ sh
sudo /opt/kubernetes/bin/kubecfg -h http://127.0.0.1:8080 list /pods
~~~
Here we can see a pod running with our app on the master node. Similarly we can do this on the other 2 nodes to access the app from all three nodes.
And we're done!!!!

