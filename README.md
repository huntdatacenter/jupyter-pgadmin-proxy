# jupyter-pgadmin-proxy

jupyter-pgadmin-proxy provides Jupyter extension to run [pgAdmin 4](https://pypi.org/project/pgadmin4/). See also official pages for ([pgAdmin](https://www.pgadmin.org/).

## Installation

You can install jupyter-pgadmin-proxy inside your environment with Jupyter / Jupyterlab:

```
python3 -m pip install git+https://github.com/huntdatacenter/jupyter-pgadmin-proxy.git@main
```

## Development

Try `make help` to see available commands:

```
make help
```

## Testing in docker

Run/rebuild local Jupyterlab service:

```
make rebuild
```

Running the command should open a url in the browser http://127.0.0.1:8888/lab

To stop the service run:
```
make down
```

