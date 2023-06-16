import os
import logging
import shutil
import pwd
import getpass
import site

logging.basicConfig(level="INFO")
logger = logging.getLogger("pgadmin")
logger.setLevel("INFO")


def _get_env(port, base_url):
    """
    Returns a dict containing environment settings to launch the Web App.
    Args:
        port (int): Port number on which the Web app will be started. Ex: 8888
        base_url (str): Controls the prefix in the url on which
                        the Web App will be available.
                        Ex: localhost:8888/base_url/index.html
    Returns:
        [Dict]: Containing environment settings to launch the Web application.
    """
    logger.info(f"pgAdmin ENV: {base_url}pgadmin4/")

    default_email = os.getenv("PGADMIN_DEFAULT_EMAIL", "pgadmin4@pgadmin.org")
    setup_email = os.getenv("PGADMIN_SETUP_EMAIL", "pgadmin4@pgadmin.org")
    return {
        "PGADMIN_SERVER_MODE": 'True',
        "PGADMIN_DEFAULT_EMAIL": default_email,
        "PGADMIN_SETUP_EMAIL": setup_email,
        "PGADMIN_SETUP_PASSWORD": "",
        "PGADMIN_LISTEN_PORT": str(port),
        "APPLICATION_ROOT": f"{base_url}pgadmin4/",
        "SCRIPT_NAME": f"{base_url}pgadmin4/",
        "REMOTE_USER": os.getenv("USER", os.getenv("NB_USER", "nobody")),
    }


def get_icon_path():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "pgadmin.svg"
    )



def get_system_user():
    try:
        user = pwd.getpwuid(os.getuid())[0]
    except Exception:
        user = os.getenv('USER', getpass.getuser())
    return user


def run_app():
    """
    Setup application.
    This method is run by jupyter-server-proxy package to launch the Web app.
    """

    logger.info("Initializing Jupyter pgAdmin Proxy")

    icon_path = get_icon_path()
    try:
        executable_name = shutil.which("pgadmin4")
    except Exception:
        executable_name = "pgadmin4"
    host = "127.0.0.1"
    user = get_system_user()
    try:
        chdir_path = f"{site.getsitepackages()[0]}/pgadmin4"
        if not os.path.exists(chdir_path):
            chdir_path = os.path.dirname(os.path.abspath(__file__))
    except Exception:
        chdir_path = "/"
    logger.debug(f"[{user}] Icon_path:  {icon_path}")
    logger.debug(f"[{user}] Launch Command: {executable_name}")
    return {
        "command": [
            # executable_name,
            "uwsgi",
            "--http-socket", "127.0.0.1:{port}",
            "--mount", "{base_url}pgadmin4/=pgAdmin4:app",
            "--chdir", chdir_path,
            "--manage-script-name",
            "--processes", "1",
            "--threads", "25",
            "--need-app",
        ],
        "timeout": 300,
        "environment": _get_env,
        "absolute_url": True,
        # "rewrite_response": rewrite_netloc,
        # "request_headers_override": {"X-Script-Name": "{base_url}pgadmin4/"},
        "launcher_entry": {
            "title": "pgAdmin4",
            "icon_path": icon_path
        },
    }
