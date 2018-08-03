docker build -t foamliu/brain-add-web:$(tag) .
docker push  foamliu/brain-add-web:$(tag)
docker run -it -p 5001:5001 foamliu/brain-add-web:$(tag)
kubectl set image deployment/brain-add-web brain-add-web=foamliu/brain-add-web:$(tag)
kubectl rollout status deploy/brain-add-web

kubectl get service brain-add-web --watch