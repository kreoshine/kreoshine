"""
Package contain different tasks for deployment
"""
from deploy.tasks.connection import echo_host
from deploy.tasks.preparatory import make_preparation, install_docker
from deploy.tasks.service_lifting import configure_nginx
