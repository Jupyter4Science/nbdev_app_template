# Scientific Web Application Template - nbdev_app_template

> A Python code example for building web apps without writing HTML, CSS. and JavaScript.

<table><tr><td width="14%">
    <img src="https://www.python.org/static/img/python-logo.png" alt="python logo">
    </td><td width="14%">
    <img src="https://altair-viz.github.io/_static/altair-logo-light.png" alt="altair viz logo
">
    </td><td width="14%">
    <img src="https://nbdev.fast.ai/assets/images/company_logo.png" alt="fast ai logo">
    </td><td width="14%">
    <b>ipywidgets</b>
    </td><td width="14%">
    <img src="https://jupyter.org/assets/logos/rectanglelogo-greytext-orangebody-greymoons.svg" alt="jupyter logo">
    </td><td width="10%">
    <img src="https://raw.githubusercontent.com/voila-dashboards/voila/main/docs/source/voila-logo.svg" alt="voila logo">
    </td><td width="14%">
    <img src="https://www.docker.com/sites/default/files/d8/styles/role_icon/public/2019-07/horizontal-logo-monochromatic-white.png" alt="docker logo">
</td></tr></table>

Got a Python project or Jupyter notebook? Want to turn it into a web applilcation?

This repository contains easy-to-modify [Python](https://www.python.org/) code. It demonstrates using [ipywidgets](https://ipywidgets.readthedocs.io/en/stable/) to build an interactive web application. It relies on [Jupyter](https://jupyter.org/) notebook infrasturcture. However, the app looks like a web app, not a notebook. Further, it demonstrates the use of [Docker](https://www.docker.com/) and [Voilà](https://github.com/voila-dashboards/voila) to allow the app to be hosted on composable infrastructure. The example code uses [pandas](https://pandas.pydata.org/) for data access and [Matplotlib](https://matplotlib.org/) to generate plots.

The template was developed so researchers can quickly and easily put their project on the web without getting bogged down in conventional web developement (AJAX, HTML, CSS, JS, etc.). The example notebook uses global temperature data from NASA to show how users can view, search, download, and plot data using an interactive, web enabled tool.


## Opinionated Development Environment

[nbdev](https://nbdev.fast.ai/) is a library originally intended to allow developers to develop python libraries from Jupyter Notebooks. The advantage of this approach is that the resulting programming environment is truely literate: all code, tests, and documentation are produced from a narrative-style composition.

Development in Notebooks is often eshewed by programmers who have a prefered IDE or development environment that has useful features such as grammar check, auto-complete, navigating by definitions, or searching code. This is a fair point, though as we will see, many or all of these features can be reclaimed through the use of extensions.

Weighing benefits and drawbacks of the use of notebooks to develop a simple library is not in the scope of this template. However, the development of a user interface in Jupyter built with ipywidgets is more cumbersome. Though the creators of nbdev may not have intended it, this library is also excellent for developing interactive applications build with [ipywidgets](https://ipywidgets.readthedocs.io/en/stable/). Because interactive widgets make heavy use of callback functions, the use of debuggers is difficult. Additionally, the notebook kernel must be restarted to propogate changes made to the codebase. We claim that nbdev is best suited to ameliorate the following tiresome development procedure:

1. Change a single line of code in a python script
2. Restart rerun the application notebook
3. Click through the application to debug and test your changes

This procedure is obviated by the use of nbdev, which allows the developer to develop, interact with, and test a subset of widgets as a single component that can be later integrated into the broader application.

## Development

### Getting Started

1. Click the "Use This Template" Button in GitHub to create a copy of this repo of your own.
1. Install [Docker](https://docs.docker.com/get-docker/) on your workstation. Note that you may need admin access to run Docker commands.
1. Start a command line (terminal) session.
1. Make sure Docker is running by entering: [`docker info`](https://docs.docker.com/config/daemon/).
1. Run `docker-compose up jupyterlab` to start the JupyterLab server.
1. Copy the URL starting with "http://localhost..." into your local browser. This URL ends with long token you will need to access the session.

### Developing on a Remote server

If you need to develop your application on a remote server - such as a compute cluster - you will need to use ssh port forwarding in order to access the notebook from the browser on your local machine.

1. SSH into the remote node using `ssh -L 8888:localhost:8888 <username>@<ip-address>`
1. Follow the steps in [Getting Started](#getting-started) ***on the remote node*** you just logged into. Docker may already be installed there. You can check for it by running `docker info`.

### Installing dependecies
Install any dependencies you need by adding them to the environment.yml file in the root directory and rebuilding the docker image.

### Upload container

To allow others to run your app, it must be hosted on a publicly available Docker hosting system. There are a wide variety of options available including commercial sites like Amazon's AWS. Some institutions maintain their own Docker hosting systems. Depending on the specific reqirements of the hosting system you select, you'll need to provide either:
- a `Dockerfile` similar to [Dockerfile-voila](Dockerfile-voila)
- a Docker image that can [hosted and pulled from Docker Hub](https://docs.docker.com/docker-hub/).
You might be required to access the host system's Kubernetes management system (e.g. Rancher) to create the container and allocate resources.

## Attributions

This template is adapted from [@rcpurdue](https://github.com/rcpurdue)'s Notebook Application Template ([nbtmpl](https://github.com/rcpurdue/nbtmpl)).
