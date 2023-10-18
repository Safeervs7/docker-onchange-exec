#!/usr/local/bin/python
import os
import hashlib
import time
import sys
import docker
docker_client = docker.from_env()

# Function to calculate the checksum of a file
def calculate_checksum(container_name, file_path):
    command_to_run = f"md5sum {file_path}"
    exec_result = run_command(container_name, command_to_run)
    checksum = exec_result.split()[0]
    return checksum

# Function to run specified command
def run_command(container_name, command):
    container = docker_client.containers.get(container_name)
    exec_result = container.exec_run(command, stdout=True, stderr=True, tty=True, detach=False)
    return exec_result.output.decode('utf-8')

# Check if any of the specified files has changed
def check_for_changes(container_name, files):
    for file_path in files:
        current_checksum = calculate_checksum(container_name, file_path)
        if checksums.get(file_path) != current_checksum:
            print(f'File {file_path} has changed.')
            return True
    return False

if __name__ == "__main__":
    # Get files and command from environment variables
    files_to_check = os.environ.get('FILES_TO_CHECK', '').split()
    command_to_check = os.environ.get('COMMAND_TO_CHECK', '')
    command_to_run = os.environ.get('COMMAND_TO_RUN', '')
    sleep_interval = int(os.environ.get('SLEEP_INTERVAL', 60)) # default 60 sec
    container_name = os.environ.get('CONTAINER_NAME', '')


    if not files_to_check or not command_to_run or not command_to_check:
        print("Please provide CONTAINER_NAME, FILES_TO_CHECK, COMMAND_TO_CHECK and COMMAND_TO_RUN environment variables.")
        sys.exit(1)

    print('FILES_TO_CHECK', files_to_check)
    print('COMMAND_TO_CHECK', command_to_check)
    print('COMMAND_TO_RUN', command_to_run)
    print('SLEEP_INTERVAL', sleep_interval)
    print('CONTAINER_NAME', container_name)


    # Calculate initial checksums
    checksums = {file_path: calculate_checksum(container_name, file_path) for file_path in files_to_check}

    try:
        while True:
            check_command_result = run_command(container_name, command_to_check)
            print('COMMAND_TO_CHECK RESULT: ', check_command_result )
            if check_for_changes(container_name, files_to_check):
                exec_result = run_command(container_name, command_to_run)
                print('COMMAND_TO_RUN RESULT: ', exec_result )
                # Update checksums after running the command
                checksums = {file_path: calculate_checksum(container_name, file_path) for file_path in files_to_check}
            time.sleep(sleep_interval)  # Wait for SLEEP_INTERVAL before the next iteration
    except KeyboardInterrupt:
        print("\nStopping the script.")
