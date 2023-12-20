TAG = admission-webhook-example:v1

linux:
	CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -a -installsuffix cgo -o admission-webhook-example
	# docker image rm $(TAG)
	docker build --no-cache -t $(TAG) .
	rm -f admission-webhook-example

load:
	kind load docker-image $(TAG)

cert:
	sh deployment/webhook-create-signed-cert.sh

deploy:
	kubectl apply -f deployment/rbac.yaml
	kubectl apply -f deployment/service.yaml
	kubectl apply -f deployment/deployment.yaml

nslabel:
	kubectl label ns default admission-webhook-example=enabled

deployvalidwebhook:
	cat deployment/validatingwebhook.yaml | ./deployment/webhook-patch-ca-bundle.sh > ./deployment/validatingwebhook-ca-bundle.yaml
	kubectl apply -f deployment/validatingwebhook-ca-bundle.yaml

deploymutatewebhook:
	cat deployment/mutatingwebhook.yaml | ./deployment/webhook-patch-ca-bundle.sh > ./deployment/mutatingwebhook-ca-bundle.yaml
	kubectl apply -f deployment/mutatingwebhook-ca-bundle.yaml