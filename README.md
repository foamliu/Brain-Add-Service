# 脑补服务

脑补是视觉认知的子集，这类任务特点是 输出信息量 > 输入。下面是一些例子：

- 黑白照片着色
- 超分辨率重建
- 自动抠图
- 注意力与显著性
- P掉XX -> 补绘
- 视频插帧
- 空间感知


## 如何使用
### 构建容器

```bash
docker build -t foamliu/brain-add-web:v0.0.7 .
docker push  foamliu/brain-add-web:v0.0.7
docker run -it -p 5001:5001 foamliu/brain-add-web:v0.0.7
```

### 部署 Kubernetes 集群

```bash
az group create --name myAKSCluster --location eastus
az aks create --resource-group myAKSCluster --name myAKSCluster --node-count 1 --generate-ssh-keys
az aks get-credentials --resource-group myAKSCluster --name myAKSCluster
kubectl get nodes
```

### 部署脑补服务

```bash
kubectl apply -f brain-add-web.yaml
kubectl get service brain-add-web --watch

kubectl set image deployment/brain-add-web brain-add-web=foamliu/brain-add-web:v0.0.7
kubectl rollout status deploy/brain-add-web

kubectl get service brain-add-web --watch
```