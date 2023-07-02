"""
Jobs that lift different services
"""
import logging

from ansible import AnsibleExecutor
from ansible.exceptions import AnsibleExecuteError
from deploy import deploy_const
from deploy.deploy_const import PROJECT_ROOT_PATH
from settings import config

logger = logging.getLogger('ansible_deploy')


async def init_nginx_container(ansible: AnsibleExecutor) -> None:
    """ Configures nginx
    Args:
        ansible: instance of ansible executor
    """
    nginx_container_name = config.deploy.nginx.container_name

    if config.deploy.mode == deploy_const.DEVELOPMENT_MODE:
        try:  # check if container exists
            await ansible.ansible_module.execute_command(
                command=f"docker container start {nginx_container_name}"
            )
            already_exist = True
        except AnsibleExecuteError:
            already_exist = False
        if already_exist:
            logger.debug("Container '%s' already exist", nginx_container_name)
            container_name = nginx_container_name
            local_root_to_static = str(PROJECT_ROOT_PATH.joinpath('frontend/app/main/'))
            root_path_for_main = '/var/www/kreoshine/'  # defined in the playbook, without 'main/' to avoid repeated dir
            await ansible.ansible_module.execute_command(
                command=f"docker cp {local_root_to_static} {container_name}:{root_path_for_main}"
            )
            logger.debug("Static files were updated, set necessary permissions")
            await ansible.ansible_module.execute_command(
                command=f"docker exec -it {container_name} sh -c 'chown nginx:nginx -R {root_path_for_main}'"
            )
            logger.info("Successfully update static files on %s container", nginx_container_name)
            return

    nginx_image_name = config.deploy.nginx.image_name
    logger.debug("Create custom nginx image '%s' on a %s host", nginx_image_name, ansible.target_host_pattern)
    create_nginx_image_task = ansible.ansible_playbook.up_nginx_container(
        local_root_to_static=str(PROJECT_ROOT_PATH.joinpath('frontend/app/main')),
        local_nginx_deploy_files_dir=str(PROJECT_ROOT_PATH.joinpath('deploy/nginx')),
        image_name=nginx_image_name,
        container_name=nginx_container_name,
    )
    await create_nginx_image_task
    logger.info("Successfully create '%s' image", nginx_image_name)
    logger.info("Successfully up '%s' container", nginx_container_name)
