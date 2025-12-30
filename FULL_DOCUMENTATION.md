### 1. Initial Setup

- **Push code to GitHub**  
  Push your project code to a GitHub repository.

- **Create a Dockerfile**  
  Write a `Dockerfile` in the root of your project to containerize the app.

- **Create Kubernetes Deployemtn file**  
  Make a file named 'llmops-k8s.yaml' 

- **Create a VM Instance on Google Cloud**

  - Go to VM Instances and click **"Create Instance"**
  - Name: ``
  - Machine Type:
    - Series: `E2`
    - Preset: `Standard`
    - Memory: `16 GB RAM`
  - Boot Disk:
    - Change size to `256 GB`
    - Image: Select **Ubuntu 24.04 LTS**
  - Networking:
    - Enable HTTP and HTTPS traffic

- **Create the Instance**

- **Connect to the VM**
  - Use the **SSH** option provided to connect to the VM from the browser.



### 2. Configure VM Instance

- **Clone your GitHub repo**

  ```bash
  git clone https://github.com/data-guru0/TESTING-9.git
  ls
  cd TESTING-9
  ls  # You should see the contents of your project
  ```

- **Install Docker**

  - Search: "Install Docker on Ubuntu"
  - Open the first official Docker website (docs.docker.com)
  - Scroll down and copy the **first big command block** and paste into your VM terminal
  - Then copy and paste the **second command block**
  - Then run the **third command** to test Docker:

    ```bash
    docker run hello-world
    ```

- **Run Docker without sudo**

  - On the same page, scroll to: **"Post-installation steps for Linux"**
  - Paste all 4 commands one by one to allow Docker without `sudo`
  - Last command is for testing

- **Enable Docker to start on boot**

  - On the same page, scroll down to: **"Configure Docker to start on boot"**
  - Copy and paste the command block (2 commands):

    ```bash
    sudo systemctl enable docker.service
    sudo systemctl enable containerd.service
    ```

- **Verify Docker Setup**

  ```bash
  systemctl status docker       # You should see "active (running)"
  docker ps                     # No container should be running
  docker ps -a                 # Should show "hello-world" exited container
  ```


### 3. Configure Minikube inside VM

- **Install Minikube**

  - Open browser and search: `Install Minikube`
  - Open the first official site (minikube.sigs.k8s.io) with `minikube start` on it
  - Choose:
    - **OS:** Linux
    - **Architecture:** *x86*
    - Select **Binary download**
  - Reminder: You have already done this on Windows, so you're familiar with how Minikube works

- **Install Minikube Binary on VM**

  - Copy and paste the installation commands from the website into your VM terminal

- **Start Minikube Cluster**

  ```bash
  minikube start
  ```

  - This uses Docker internally, which is why Docker was installed first

- **Install kubectl**

  - Search: `Install kubectl`
  - Run the first command with `curl` from the official Kubernetes docs
  - Run the second command to validate the download
  - Instead of installing manually, go to the **Snap section** (below on the same page)

  ```bash
  sudo snap install kubectl --classic
  ```

  - Verify installation:

    ```bash
    kubectl version --client
    ```

- **Check Minikube Status**

  ```bash
  minikube status         # Should show all components running
  kubectl get nodes       # Should show minikube node
  kubectl cluster-info    # Cluster info
  docker ps               # Minikube container should be running
  ```

### Setup firewall GCP
- If the page doesn't load, set a firewall rule: GCP → VPC Network → Firewall → Create Firewall Rule
- Name: allow-jenkins
- Description: Allow all traffic (for Jenkins demo)
- Logs: Off
- Network: default
- Direction: ingress
- Action: allow
- Targets: All instances
- Source IP ranges: 0.0.0.0/0
- Allowed protocols and ports: all

### 4. Interlink your Github on VSCode and on VM

```bash
git config --global user.email "my_email@gmail.com"
git config --global user.name "my_username"

git add .
git commit -m "commit"
git push origin main
```

- When prompted:
  - **Username**: `my_username`
  - **Password**: GitHub token (paste, it's invisible) - nhập token được tạo từ bước dưới đây :

- chỗ nhập **Password** ta sẽ không nhập password mà trong github ta sẽ chọn settings -> Developer Setting -> Tokens(classic) -> New personal access token (classic) -> chọn các quyền sau - chọn quyền dưới rồi mới tiếp tục -> Generate token -> nó sẽ tạo ra token và chỉ cần copy paste vào password bên trên:
    - repo
    - workflow
    - admin:org 
    - admin:repo_hook
    - admin:org_hook
---


### 5. Build and Deploy your APP on VM

```bash
## Point Docker to Minikube
eval $(minikube docker-env)

docker build -t llmops-app:latest .

kubectl create secret generic llmops-secrets \
  --from-literal=GROQ_API_KEY="api_key" \
  --from-literal=HUGGINGFACEHUB_API_TOKEN="api_key" 
# chạy 2 dòng này xong nó sẽ ra  secret/llmops-secrets create nên trong file llmops-k8s.yaml phần envFrom ta lại để tên là name : llmops-secrets


kubectl apply -f llmops-k8s.yaml


kubectl get pods

### U will see pods runiing


# Do minikube tunnel on one terminal

minikube tunnel


# chạy lệnh trên gcp
kubectl get svc # lệnh này cho ra các cân bằng tải và chúng ta chọn llmops-service - nên ở dưới mới có svc/llmops-service
# Open another terminal
kubectl port-forward svc/llmops-service 8501:80 --address 0.0.0.0

## Now copy external ip and :8501 and see ur app there....


```

### 6. GRAFANA CLOUD MONITORING

```bash
## Open another VM terminal for Grfana cloud

kubectl create ns monitoring

kubectl get ns

## Make account on Grfaana cloud

### Install HELM - Search on Google
-- Copy commands from script section..
-- U will get 3 commands


## Come to grafana cloud --> Left pane observability --> Kubernetes--> start sending data
## In backend installation --> Hit install
## Give your clustername and namespace there : minikube and monitoring in our case
## Select kubernetes
## Keep other things on as default
## Here only create new access token give name lets give minikube-token & Create it and save it somewhere..
## Select helm and deploy helm charts is already generated...



## Come to terminal --> Create a file
vi values.yaml


## Paste all from there to your file now remove last EOF part & and also initial part save that initial part we need it..

Example : 

helm repo add grafana https://grafana.github.io/helm-charts &&
  helm repo update &&
  helm upgrade --install --atomic --timeout 300s grafana-k8s-monitoring grafana/k8s-monitoring \
    --namespace "monitoring" --create-namespace --values - <<'EOF'

### Remove this above intial part and save it somewhere

Then Esc+wq! amd save the file


## Now use the copied command just make some modification:
Remove that EOF part and instead write
--values values.yaml

Example:

helm repo add grafana https://grafana.github.io/helm-charts &&
  helm repo update &&
  helm upgrade --install --atomic --timeout 300s grafana-k8s-monitoring grafana/k8s-monitoring \
    --namespace "monitoring" --create-namespace --values values.yaml

## Paste this command on VM u will get status deployed revision 1
## It means it was a SUCESS

To check:

kubectl get pods -n monitoring

# These are all should be running.....

Go to grafana cloud again..
And below u will get go to homepage click it..
Just refresh the page and boom..


Now u can see metrics related to your kubernetes cluster..

---Explore it for yourself now 

---Make sure to do cleanup 

```