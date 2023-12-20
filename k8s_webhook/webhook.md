# webhook demo

kind-config.yaml

```yml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
```

```sh
# 创建集群
kind create cluster --config=kind-config.yaml

# 检查是否开启了准入控制
apiserver_pod_name=$(kubectl -n kube-system --no-headers=true get pod | grep apiserver | awk '{print $1}')
kubectl -n kube-system --no-headers=true get pod $apiserver_pod_name -oyaml | grep plugins

# 输出如下
- --enable-admission-plugins=NodeRestriction

# kind 创建的 K8S 默认是没有的开启准入控制的，所以需要修改 apiserver 的启动参数
controlplane=$(docker ps --format '{{.ID}} {{.Names}}' | grep control | awk '{print $1}')

# 进去 controlplane 修改 kube-apiserver.yaml 配置文件
docker exec -it $controlplane /bin/bash

apt update -y && apt install vim -y

# 修改 apiserver 的启动参数
vi /etc/kubernetes/manifests/kube-apiserver.yaml

# 新增这两个 plugin
MutatingAdmissionWebhook,ValidatingAdmissionWebhook

# 然后重启 controlplane
docker stop $controlplane
docker start $controlplane

# 再次检查
kubectl -n kube-system --no-headers=true get pod $apiserver_pod_name -oyaml | grep plugins

# 如果输出如下，说明已经开启好了
- --enable-admission-plugins=NodeRestriction,MutatingAdmissionWebhook,ValidatingAdmissionWebhook
```

证书认证

apiserver 调用 webhook 的过程是走的 HTTPS ，所以需要配置证书认证，证书认证是给 service 的域名进行认证

将 service 的域名放到认证请求文件中，然后创建一个 K8S 证书签署请求资源 csr(CertificateSigningRequest)

apiserver 签署该证书，详细过程看脚本 webhook-create-signed-cert.sh

```sh
./deployment/webhook-create-signed-cert.sh
creating certs in tmpdir /var/folders/ns/f_24jl8s6ts7qx6gvwwl7jjr0000gn/T/tmp.UN47NWcc
certificatesigningrequest.certificates.k8s.io/admission-webhook-example-svc.default created
NAME                                    AGE   SIGNERNAME                      REQUESTOR          REQUESTEDDURATION   CONDITION
admission-webhook-example-svc.default   0s    kubernetes.io/kubelet-serving   kubernetes-admin   <none>              Pending
certificatesigningrequest.certificates.k8s.io/admission-webhook-example-svc.default approved
W1218 20:19:55.317502   82158 helpers.go:663] --dry-run is deprecated and can be replaced with --dry-run=client.
secret/admission-webhook-example-certs created
```

部署 deployment

```sh
# 构建镜像
sh build.sh

# 把本地镜像导入到集群中
kind load docker-image admission-webhook-example:v1

# webhook 会对资源进行修改，所以需要单独配置一个 sa
kubectl apply -f deployment/rbac.yaml

# 创建 webhook 的 deploy 和 service
kubectl apply -f deployment/deployment.yaml
kubectl apply -f deployment/service.yaml
```

验证 validate

```sh
# 配置 validate webhook
cat deployment/validatingwebhook.yaml | ./deployment/webhook-patch-ca-bundle.sh > ./deployment/validatingwebhook-ca-bundle.yaml
kubectl apply -f deployment/validatingwebhook-ca-bundle.yaml

# 由于 webhook 中配置了 namespaceSelector 
# 所以 webhook 只适用于 admission-webhook-example=enabled 标签的 namespace
# 所以需要给 default 这个 namespace 添加标签
kubectl label ns default admission-webhook-example=enabled

# 验证 没有标签
kubectl apply -f deployment/nginx.yaml
Error from server (required labels are not set): error when creating "deployment/nginx.yaml": admission webhook "required-labels.neverdown.com" denied the request: required labels are not set

# 验证 没有 limit/request 配置
kubectl apply -f deployment/nginx-no-resource.yaml
Error from server (required limit/request are not set): error when creating "deployment/nginx-no-resource.yaml": admission webhook "required-labels.neverdown.com" denied the request: required limit/request are not set

# 验证 有标签和 limit/request 配置
kubectl apply -f deployment/nginx-with-label.yaml

# 可以看到 nginx 的 Pod 创建正常
kubectl get pod
NAME                                                    READY   STATUS    RESTARTS   AGE
admission-webhook-example-deployment-695bdc9788-5d67f   1/1     Running   0          2m17s
nginx-6c5d46bcb5-2brh8                                  1/1     Running   0          38s

# 验证 跳过 validate 也能正常创建
kubectl apply -f deployment/nginx-no-valiedate.yaml
deployment.apps/nginx created
```

验证 mutate

```sh
# 配置 mutate webhook
cat deployment/mutatingwebhook.yaml | ./deployment/webhook-patch-ca-bundle.sh > ./deployment/mutatingwebhook-ca-bundle.yaml
kubectl apply -f deployment/mutatingwebhook-ca-bundle.yaml

# 验证 没有标签
kubectl apply -f deployment/nginx.yaml

# 会看到已经自动给补充上了
kubectl get deploy --show-labels
NAME                                   READY   UP-TO-DATE   AVAILABLE   AGE   LABELS
admission-webhook-example-deployment   1/1     1            1           10m   app=admission-webhook-example
nginx                                  1/1     1            1           72s   app.kubernetes.io/component=not_available,app.kubernetes.io/instance=not_available,app.kubernetes.io/managed-by=not_available,app.kubernetes.io/name=not_available,app.kubernetes.io/part-of=not_available,app.kubernetes.io/version=not_available
```
