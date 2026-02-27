# Secure Kubernetes API Platform

## Overview

This project demonstrates a production-grade, self-managed API platform
built using:

-   Kubernetes (Declarative resources only)
-   Kong Gateway (DB-less mode)
-   JWT Authentication (Externalized secret via Helm)
-   Rate Limiting (IP-based)
-   IP Whitelisting
-   Custom Lua Plugin
-   Envoy-based DDoS Protection
-   Fully Helm-managed deployments

------------------------------------------------------------------------

## Architecture Diagram

![Architecture
Diagram](Architecture.png)

------------------------------------------------------------------------

## Components

### 1️⃣ User Service

-   FastAPI-based microservice
-   Issues JWT tokens
-   Verifies JWT tokens
-   `/health` and `/verify` endpoints bypass gateway authentication

### 2️⃣ Kong Gateway

-   DB-less declarative configuration
-   JWT Plugin enabled for protected routes
-   Rate limiting: 10 requests/min per IP
-   IP restriction policy
-   Custom Lua logic for header injection / structured logging

### 3️⃣ Envoy (DDoS Protection Layer)

-   Connection limiting
-   Rate control
-   Acts as first-line defense before Kong

------------------------------------------------------------------------

## Security Features

-   JWT secret injected via Helm (`--set jwtSecret=$JWT_SECRET`)
-   No hardcoded secrets in repository
-   IP-based traffic control
-   Rate limiting at gateway level
-   DDoS mitigation at ingress layer

------------------------------------------------------------------------

## Deployment Steps

### Create Docker Image

``` bash
cd microservice
docker build -t <repository_name>:latest .
docker push <repository_name>
```

### Deploy EKS Cluster Using Terraform

``` bash
cd terraform
terraform init
terraform plan
terraform apply
```

### Connect kubectl to EKS

``` bash
aws eks update-kubeconfig --region <region> --name <cluster_name>
``` 

### Deploy Using minikube

``` bash
Install minikube on local terminal
```

### Create JWT Secrets and ADMIN_PASSWORD

``` bash
export JWT_SECRET=$(openssl rand -hex 32)
export ADMIN_PASSWORD=$(openssl rand -base64 16)
```

### Deploy User Service, Kong and Envoy via Helm

``` bash
helm upgrade --install user-service ./helm/user-service --set jwtSecret="$JWT_SECRET" --set adminPassword="$ADMIN_PASSWORD"
helm upgrade --install kong ./helm/kong --set jwtSecret="$JWT_SECRET"
helm upgrade --install envoy ./helm/envoy
```

### Verify Running Pod ad Services

``` bash
kubectl get pod
kubectl get svc
```

------------------------------------------------------------------------

## Functional Verification/Testing 

``` bash
minikube ip
export URL=http://<minikube_ip:envoy_port>
```

### 1. Health Check Status

``` bash
curl $URL/health
```

### 2. Get Token

``` bash
curl -X POST $KONG_URL/login -H "Content-Type: application/json" -d '{"username":"admin","password":"'$ADMIN_PASSWORD'"}'
```

### 3. Test Access Protected API With and Without Token

``` bash
curl $URL/users
curl $URL/users -H "Authorization: Bearer <TOKEN>"
```

### 4. Validate Token

``` bash
curl $URL/verify
curl $URL/verify -H "Authorization: Bearer <TOKEN>"
```

### 5. Test Rate Limiting (10 per minute)

``` bash
for i in {1..15}; do
  curl -s -o /dev/null -w "%{http_code}\n" $URL/health
done
```

### 6. DDoS Simulation

``` bash
ab -n 10 -c 5 -k $URL/
```
------------------------------------------------------------------------

## Project Structure

├── Architecture.png
├── README.md
├── ai-usage.md
├── helm
│   ├── envoy
│   │   ├── Chart.yaml
│   │   ├── envoy.yaml
│   │   ├── templates
│   │   │   ├── configmap.yaml
│   │   │   ├── deployment.yaml
│   │   │   └── service.yaml
│   │   └── values.yaml
│   ├── kong
│   │   ├── Chart.yaml
│   │   ├── kong.yaml
│   │   ├── plugins
│   │   │   └── custom.lua
│   │   ├── templates
│   │   │   ├── configmap.yaml
│   │   │   ├── deployment.yaml
│   │   │   ├── secret.yaml
│   │   │   └── service.yaml
│   │   └── values.yaml
│   └── user-service
│       ├── Chart.yaml
│       ├── templates
│       │   ├── deployment.yaml
│       │   ├── secret.yaml
│       │   └── service.yaml
│       └── values.yaml
├── microservice
│   ├── Dockerfile
│   ├── app
│   │   └── main.py
│   └── requirements.txt
└── terraform
    ├── main.tf
    ├── outputs.tf
    ├── terraform.tfvars
    └── variables.tf

------------------------------------------------------------------------

## Author

Gopal Bugad
