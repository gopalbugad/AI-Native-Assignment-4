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

## Deployment

``` bash
export JWT_SECRET=$(openssl rand -hex 32)

helm upgrade --install user-service ./helm/user-service
helm upgrade --install kong ./helm/kong --set jwtSecret=$JWT_SECRET
helm upgrade --install envoy ./helm/envoy
```

------------------------------------------------------------------------

## Testing

### Get Token

``` bash
curl -X POST $KONG_URL/login   -H "Content-Type: application/json"   -d '{"username":"admin","password":"admin"}'
```

### Access Protected API

``` bash
curl $KONG_URL/users -H "Authorization: Bearer <TOKEN>"
```

### DDoS Simulation

``` bash
ab -n 100 -c 20 $KONG_URL/users
```

------------------------------------------------------------------------

## Project Structure

    helm/
      kong/
      user-service/
      envoy/
    microservice/
      app/main.py

------------------------------------------------------------------------

## Author

Gopal Bugad
