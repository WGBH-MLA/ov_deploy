from subprocess import run as sub_run
from pydantic import BaseModel

GITHUB_URL = 'https://github.com/WGBH-MLA/'
OV_WAG_URL = GITHUB_URL + 'ov_wag.git'
OV_FRONT_URL = GITHUB_URL + 'ov-frontend.git'
HUB_ACCOUNT = 'wgbhmla'


def run(cmd: str):
    sub_run(cmd, shell=True, check=True)


class Deployer(BaseModel):
    """Deployer class

    Used for openvault deployment configuration
    """

    context: str
    ov_wag: str = None
    ov_wag_env: str = None
    ov_wag_secrets: str = None
    ov_frontend: str = None
    ov_frontend_env: str = None
    ov_nginx: str = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_current_context()

    def set_current_context(self):
        """Switch to the specified kubectl context."""
        run(f'kubectl config use-context {self.context}')

    def build_image(self, repo_name, tag, src=''):
        """Build and tag docker image from a repo#tag"""
        run(f'docker build {src or repo_name} -t {HUB_ACCOUNT}/{repo_name}:{tag}')

    def push_image(self, repo_name, tag):
        """Push a tagged docker image to hub.docker.com

        Requires the user to be logged in"""
        run(f'docker push {HUB_ACCOUNT}/{repo_name}:{tag}')

    def update_workload(self, pod, tag):
        """Sets the backend pod image to the proper tag"""
        run(f'kubectl set image deployment.apps/{pod} {pod}={HUB_ACCOUNT}/{pod}:{tag}')

    def _deploy(self, repo_name, tag, src=''):
        """Deploy helper function

        Deploy an individual image from a repo and tag name"""
        self.build_image(repo_name, tag, src=src)
        self.push_image(repo_name, tag)
        self.update_workload(pod=repo_name, tag=tag)

    def deploy(self):
        """Deploy all

        Run the full deployer process using the current context"""
        print(f'Starting deployment using context "{self.context}"')

        if not any([self.ov_wag, self.ov_frontend, self.ov_nginx]):
            raise Exception(f'Nothing specified for deployment.')
        if self.ov_wag:
            self._deploy('ov_wag', self.ov_wag, src=f'{OV_WAG_URL}#{self.ov_wag}')
        if self.ov_frontend:
            self._deploy(
                'ov-frontend',
                self.ov_frontend,
                src=f'{OV_FRONT_URL}#{self.ov_frontend}',
            )
        if self.ov_nginx:
            self._deploy('ov_nginx', self.ov_nginx, src='ov-nginx')

        print('Done!')
