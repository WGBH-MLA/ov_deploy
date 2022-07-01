# Deployment steps

## init

To deploy a new stack:

### 1. Create namespace in Rancher

Production: `openvault`
demo: `ov-demo`

### 2. Create pods

#### db

- image: `postgres:14.2-alpine`
- secrets:
  - `POSTGRES_PASSWORD`

#### ov (backend)

- image: `wgbhmla/ov_wag`
- config:
  - `ov_wag.config`
- secrets:
  - `OV_DB_PASSWORD`

#### ov-frontend

- image: `wgbhmla/ov-frontend`
- config:
  - `ov-frontend.config`

#### ov-nginx

- image: `foggbh/ov-nginx`
  - configured with `nginx.conf`
  - proxy pass to `http://ov-frontend:3000`
- ports:
  - `80/http`
- ingress:
  - hostname: `[url]`

#### jumpbox (optional utility kit)

- image: ?

## Redeploy

Redeployment steps for demo or production

### 0. Check out code

Set up the code to represent the state of the application you wish to redeploy.

#### Scenario #1: Redeploy an `ov_deploy` commit

These steps assume some `ov_deploy` commit should be pushed to some deployment environment, either `production` or `demo`.

Starting from a known `ov_deploy` commit or branch:

`git checkout [commit or branch]`

`git submodule update`

#### Scenario #2: Custom code

In `ov_wag` and `ov-frontend`, checkout (or manually edit) the code in each repository.

### 1. Build images

- Build all images:

  `./ov build`

- Build single image:

  `./ov build [image name]`

**_Note:_** Other custom commands can be passed into the

### 2. Push to docker hub

(tag the image?)

`docker push [tag name]`

### 3. Redeploy pods

Redeploy the pod(s)

- Rancher
- kubectl
