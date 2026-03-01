### 1. Prompt - 

``` bash
You are a Senior DevOps + Platform Engineer with deep experience in Kubernetes, Kong Gateway (OSS), API security, and cloud-native infrastructure.
I am building a self-managed, Kubernetes-based secure API platform using Kong Gateway.
The system must be production-grade, reproducible, and fully declarative.
 
Objective
Design and implement a secure API platform that exposes a sample user microservice through Kong API Gateway with:
- JWT-based authentication
- Authentication bypass for selected APIs
- IP-based rate limiting
- IP whitelisting
- Open-source, self-managed DDoS protection
- Custom Kong Lua logic
- Deployment via Helm charts
- Kubernetes-native, declarative resources only
 
Mandatory Constraints
- API Gateway must be Kong (OSS, self-managed)
- Platform must run on Kubernetes
- No imperative kubectl commands
- All configs must be version-controlled
- JWT secrets must NOT be hardcoded
- Database must be SQLite (local file-based)
- DB must auto-initialize on service startup
- Helm charts are mandatory
- Include at least one custom Kong Lua script
- Terraform for Kubernetes cluster provisioning (Use EKS)
 
Security & Traffic Requirements
Authentication
- JWT authentication via Kong JWT plugin
- JWT issued by the microservice (/login)
- /verify validates token

Authentication Bypass (MANDATORY)
The following APIs must bypass authentication at the gateway:
- GET /health
- GET /verify
Explain how the bypass works technically in Kong.
 
Traffic Protection
Rate Limiting
- IP-based rate limiting via Kong plugin
- Policy: 10 requests per minute per IP

IP Whitelisting
- Only allow traffic from configurable CIDR ranges
- Block all other traffic at the gateway level
 
DDoS Protection
- Envoy-based rate/connection controls

You must:
- Justify the choice of this DDOS protection
- Explain how it integrates with Kong + Kubernetes
- Demonstrate basic protection behavior
 
Custom Kong Lua Logic (MANDATORY)
Implement at least one Lua script, such as:
- Custom request/response header injection
- Additional JWT validation logic
- Structured request logging

Lua requirements:
- Version-controlled
- Deployed via Kong configuration
- Clearly explain execution phase (access, header_filter, log, etc.)
 
Microservice Requirements
Implement a user service with:
Authentication APIs
- POST /login → authenticate user, return JWT
- GET /verify → verify JWT

Protected API
- GET /users → JWT required

Public APIs (Auth Bypass)
- GET /health
- GET /verify

Use:
- SQLite database
- Secure password hashing
- Auto DB initialization
 
Kubernetes & Deployment
- Containerize the microservice
- Kubernetes resources:
   - Deployment
   - Service
- Helm charts for:
   - Microservice
   - Kong Gateway
- Clean, parameterized values.yaml  

Expected Directory Structure - 
.
├── microservice/
│   ├── app/
│   ├── Dockerfile
│   └── sqlite.db
├── helm/
│   ├── user-service/
│   └── kong/
├── kong/
│   ├── plugins/
│   │   └── custom.lua
│   └── kong.yaml
├── k8s/
│   └── deployment.yaml
├── terraform/        # optional
├── README.md
└── ai-usage.md


IMPORTANT NOTE -  
1 - Provide the proper code for the same first, with an explanation, and compress it in a zip file at the end.
```

### Response - 
``` bash
It provided the expalnation of code that we are going to implement with implementatiion steps.
```


### 2. Prompt - 
``` bash
what secret I can pass here(JWT_SECRET) variable and in what format it stores.
``` 

### Response -
``` bash
It shared the command from that we can create the JWT Secrect and explain how and in what format we are storing it.
``` 

### 3. Prompt -
``` bash 
Geting container failed issue for envoy deployemnt - 
Events: Type Reason Age From Message ---- ------ ---- ---- ------- Normal Scheduled 38s default-scheduler Successfully assigned default/envoy-844fcc4967-556b4 to minikube Normal Pulling 37s kubelet Pulling image "envoyproxy/envoy:v1.29-latest" Normal Pulled 19s kubelet Successfully pulled image "envoyproxy/envoy:v1.29-latest" in 17.635s (17.635s including waiting). Image size: 152240213 bytes. Normal Pulled 8s (x2 over 18s) kubelet Container image "envoyproxy/envoy:v1.29-latest" already present on machine and can be accessed by the pod Normal Created 7s (x3 over 19s) kubelet Container created Normal Started 7s (x3 over 19s) kubelet Container started Warning BackOff 7s (x3 over 17s) kubelet Back-off restarting failed container envoy in pod envoy-844fcc4967-556b4_default(0b0cdd4d-74b7-4909-94c2-63cefe641360)
```

### Response -
``` bash 
It shared the respne with actual reason beahind this container failed error - It was failed due to the invalid envoy.yaml config file. Then it resolved the issue by provind the fixed code.
``` 

### 4. Prompt -
``` bash 
All resorces are deployed and it is running now. Tell me next steps to verify this Kubernetes-based API platform that exposes a secure microservice through Kong Gateway and Envoy Proxy DDOS protection is correctly configured or not.
``` 

### Response -
``` bash 
It shared the Functional Verification/Testing steps(commands).
``` 

### 5. Prompt -
``` bash 
Create the Architecture diagram for this project
``` 

### Response -
``` bash 
Created the diagram and shared it with me.
``` 

### 6. Prompt -
``` bash 
Create the Readme.md file for me for this project
``` 

### Response -
``` bash 
Shared the created Readme.md file.
``` 