from invoke import task


@task
def run(c):
    c.run("python3 main.py")


@task
def reformat(c):
    print("invoke: reformat")
    c.run("autopep8 --in-place --aggressive -r ./")
