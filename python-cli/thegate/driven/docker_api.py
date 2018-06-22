"""
Adapter for the `docker` module
"""

import docker


class DockerApi():
    def __init__(self):
        self.docker = docker.from_env()

    def run(self, image_name, command, volumes=()):
        """ Run a container syncronously """
        self.docker.containers.run(
            image_name,
            command,
            volumes=self._map_volumes(volumes))

    def run_background(self, container_name, image_name, command, volumes=()):
        """ 
        Run a container asynchronously with the given name

        Returns:
            The container name formatted to be valid.

            Use this formatted name to operate on it in
            `is_running_background` and `stop_background`
        """
        formatted_name = self._format_name(container_name)

        self.docker.containers.run(
            image_name,
            command,
            name=formatted_name,
            detach=True,
            remove=True,
            volumes=self._map_volumes(volumes))

        return formatted_name

    def is_running_background(self, container_name):
        """ Check if a container is running in the background """
        running_container_names = [
            c.name for c in self.docker.containers.list()]
        return container_name in running_container_names

    def stop_background(self, container_name):
        """ Stop a container running in the background """
        try:
            running_container = self.docker.containers.get(container_name)
            running_container.stop()
        except docker.errors.NotFound:
            raise ContainerNotRunningError(
                "'".join([
                    'Container ',
                    container_name,
                    ' is not running and can not be stopped!']))

    @staticmethod
    def _map_volumes(volumes_tuple: tuple):
        vol_dict = {}
        for vol in volumes_tuple:
            vol_params = vol.split(':')

            vol_path = vol_params[0]
            vol_mount_pt = vol_params[1]
            if len(vol_params) > 2:
                vol_mode = vol_params[2]
            else:
                vol_mode = 'rw'

            vol_dict[vol_path] = {
                'bind': vol_mount_pt,
                'mode': vol_mode
            }

        return vol_dict

    @staticmethod
    def _format_name(container_name: str):
        return "-".join(container_name.split())


class ContainerNotRunningError(Exception):
    pass
