"""
Package contain different jobs for deployment
"""
from deploy.jobs.connection import echo_host
from deploy.jobs.preparatory import make_preparation, install_docker
from deploy.jobs.service_lifting import configure_nginx
