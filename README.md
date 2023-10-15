## Overview
This Docker repository hosts a versatile Python script (on-change.py) designed for development environment automation. The script enables automated actions based on file modifications, including triggering dev deployment through Docker, avoiding the need for continuous integration and continuous deployment (CI/CD) in a local development setup. It's a valuable tool for streamlined development workflows, enabling auto-execution of specified commands when files change, enhancing efficiency and aiding in various use cases such as:

- Dev environment auto-deployment
- Auto-reloading applications for faster development iterations
- Running test suites upon code changes
- Enabling automated actions for specific file modifications

This repository simplifies and enhances the development process by leveraging Docker and automation for seamless local development experiences.

## Usage Details:
To monitor and continuously perform git pull within the attached work-dir volume, detecting changes in the package.json file, and triggering an npm install if changes are detected, you can use the following docker run command:

```bash
docker run -ti \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v $PWD:/on-change \
    --privileged \
    -e FILES_TO_CHECK=package.json \
    -e COMMAND_TO_CHECK="/usr/bin/git pull" \
    -e COMMAND_TO_RUN="/usr/local/bin/npm install" \
    -e CONTAINER_NAME=main-app \
    -e SLEEP_INTERVAL=10 \
    redsh4d0w/docker-onchange-exec:1.0
```
### Explanation of Environment Variables:

FILES_TO_CHECK=package.json: Specifies the file to monitor for changes, in this case, package.json.

COMMAND_TO_CHECK="/usr/bin/git pull": Defines the command to check for changes, set to git pull in this example.

COMMAND_TO_RUN="/usr/local/bin/npm install": Specifies the command to execute when changes are detected, in this case, npm install.

CONTAINER_NAME=main-app: Specifies the target container where COMMAND_TO_RUN should be executed, in this example, set to main-app.

SLEEP_INTERVAL=10: Sets the interval (in seconds) at which the script checks for changes, in this case, set to every 10 seconds.

--privileged: Provides elevated privileges to the container, allowing it to perform privileged tasks.

-v /var/run/docker.sock:/var/run/docker.sock: Binds the Docker socket of the host to the Docker socket inside the container, enabling communication with the Docker daemon.

-v $PWD:/on-change: Mounts the current directory to /on-change inside the container, enabling a shared working directory between the main container and the git-on-change container. This allows seamless file sharing and monitoring, enhancing the automation of development workflows.

## Example
Explore the https://github.com/Safeervs7/docker-onchange-exec/tree/main/example example folder to understand how you can structure your project and adapt the Docker Compose configuration.

```bash
version: '2.17'
networks:
  my-network:
    name: my-network
volumes:
  work-dir:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: $PWD
services:
  main-app:
    restart: always
    container_name: main-app
    build:
      context: .
      dockerfile: ./Dockerfile
    privileged: true
    volumes:
      - 'work-dir:/work-dir'
  git-on-change:
    depends_on:
      - main-app
    restart: unless-stopped
    image: redsh4d0w/docker-onchange-exec:1.0
    privileged: true
    environment:
      - FILES_TO_CHECK=package.json
      - COMMAND_TO_CHECK=/usr/bin/git pull
      - COMMAND_TO_RUN=/usr/local/bin/npm install
      - CONTAINER_NAME=main-app
      - SLEEP_INTERVAL=10
    volumes:
      - '/var/run/docker.sock:/var/run/docker.sock'
      - 'work-dir:/on-change'
```

This configuration sets up two services: main-app and git-on-change. The git-on-change service will monitor the package.json file and automatically run git pull and npm install on main-app container when changes are detected.
