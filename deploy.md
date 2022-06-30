# Deployment steps

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
