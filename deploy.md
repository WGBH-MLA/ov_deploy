# Deployment steps

## init

To create a new stack:

### 1. Create namespace in Rancher

### 2. Create pods

- db
  - image: `postgres:14.2-alpine`
  - secrets:
    - `POSTGRES_PASSWORD`
- ov (backend)
  - image: `wgbhmla/ov_wag`
  - config:
    - `ov_wag.config`
  - secrets:
    - `OV_DB_PASSWORD`
- ov-frontend
  - image: `wgbhmla/ov-frontend`
  - config:
    - `ov-frontend.config`
- ov-nginx
  - image: `foggbh/ov-nginx`
    - configured with `nginx.conf`
    - proxy pass to `http://ov-frontend:3000`
  - ports:
    - `80/http`
  - ingress:
    - hostname: `[url]`

## deploy

Deployment steps for demo or production

### 0. Check out code

#### Scenario #1: Using Submodules

Starting from a known `ov_deploy` commit or branch:

- `git checkout [commit or branch]`
- `git submodule update`

### 1. Build images

- Build all images

  `./ov build`

- Build single image

  `./ov build [image name]`

### 2. Push to docker hub

(tag the image?)

`docker push [tag name]`

### 3. Redeploy pods

Redeploy the pod(s) in Rancher
