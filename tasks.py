from invoke import task

@task
def dev(c):
    c.run("uvicorn server:app --host 0.0.0.0 --port 3333 --reload")

@task
def dev_ssl(c):
    c.run("uvicorn server:app --host 0.0.0.0 --port 3333 --ssl-keyfile localhost-key.pem --ssl-certfile localhost.pem --reload")