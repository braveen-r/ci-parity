import platform
import subprocess
import os

def get_local_os():
    try:
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("PRETTY_NAME="):
                    return line.split("=")[1].strip().strip('"')
    except FileNotFoundError:
        pass
    return platform.system()

def get_local_python():
    return platform.python_version()

def get_local_node():
    try:
        result = subprocess.run(["node", "-v"], capture_output=True, text=True, check=True)
        return result.stdout.strip().lstrip("v")
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "not installed"

def check_local_env(env_vars):
    """Checks if required CI env vars are set locally."""
    return {var: (var in os.environ) for var in env_vars}

def check_local_services(services):
    """Checks if docker containers for required services are running."""
    status = {}
    try:
        result = subprocess.run(["docker", "ps", "--format", "{{.Names}} {{.Image}}"], capture_output=True, text=True)
        running_containers = result.stdout.lower()
        for svc in services:
            status[svc] = svc.lower() in running_containers
    except Exception:
        for svc in services:
            status[svc] = False
    return status

def get_local_state(ci_reqs):
    return {
        "os": get_local_os(),
        "python": get_local_python(),
        "node": get_local_node(),
        "env": check_local_env(ci_reqs.get("env", [])),
        "services": check_local_services(ci_reqs.get("services", {}))
    }
