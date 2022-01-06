# nbtmpl - Notebook-based App Template
A Python code example for building web apps without writing HTML, CSS. and JavaScript.

<table><tr><td width="14%">
    <img src="https://www.python.org/static/img/python-logo.png" alt="python logo">
    </td><td width="14%">
    <img src="https://pandas.pydata.org/static/img/pandas_white.svg" alt="pandas logo">
    </td><td width="14%">
    <img src="https://matplotlib.org/_static/images/logo2.svg" alt="matplotlib logo">
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

## How It Works
Source code is organized in a loose [Model-view-controller](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller) pattern. The code is divided into three classes in the "nb" directory:

- Model: Works with data and storage (file system, database, etc)
- View:  Builds the user interface (widgets, plots, etc.)
- Controller: Responds to user actions (button presses, menu selections, etc.)

The Jupyter notebook ('notebook.ipynb") contains just one code cell. This kicks off the MVC code and the web app starts running.

The code relies on [widgets](https://en.wikipedia.org/wiki/Graphical_widget) and [callbacks](https://en.wikipedia.org/wiki/Callback_(computer_programming)) methods. Once it's up and running, the code waits for the user to make changes to user interface widgets. But widget updates also work in both directions. When the user interacts with a widget in their browser, an assigned callback method runs. And when some code changes a widget, those changes appear in the browser.

For example, the view object creates a button named "filter_btn_apply". The controller specifies that, when this button is pressed, its "cb_apply_filter()" method should be called ("view.filter_btn_apply.on_click(self.cb_apply_filter)"). The "cb_apply_filter()" method then directs the model to perform the query and then updates the view's output widget, "view.filter_output".

## Develop and Test

### Install dependecies on your workstation
This project requires Python, Jupyter, and a number of Python packages. One options is to can manually install the packages listed under "dependencies" in `environment.yml`. Another option is to use the Andaconda package management system to create an isolated environment. This prevents package installations from affecting your other projects.

### (optional but encouraged): Use Conda
1. Install [Anaconda](https://www.anaconda.com/products/individual) on your workstation.
1. At the OS command line, run: `conda env create --file environment.yml`. This creates a conda environment called "nbtmpl" and installs packages into it. Answer "y" to prompts.

### Start Jupyter and run the notebook
1. Start a command line (terminal) session.
1. If using conda, enter `conda activate nbtmpl`
1. Enter `jupyter lab`. (See [Starting JupyterLab](https://jupyterlab.readthedocs.io/en/stable/getting_started/starting.html) for more info.
1. Browse to the nbtmpl directory and double click on the `notebook.ipynb` file.
1. Click the "Restart kernel...re-run...notebook" button (double trinangle icon).
1. When prompted, click the "Restart" button.
1. NOTE: Later, when the notebook and code runs as a web app, only the title, tabs, and tab content will appear. The Jupyter Lab UI and the notebook's code cell will not appear.

### Debugging

For simple bugs, use the log and [print debugging](https://en.wikipedia.org/wiki/Debugging#Techniques) (`logger.debug(...)`) to display values of variables. The log can viewed in Jupyter Lab's "Log Console" (menu: View --> Show Log Console). Specify  `log=True` when calling the view's `start()` method.

For more difficult bugs, use Jupyter Lab's [debugger](https://jupyterlab.readthedocs.io/en/stable/user/debugger.html). Set a breakpoint in a line of code in the notebook (after the import). Using the debugger, run to that breakpoing. Then, trace down into the model, view, or controller code and set more breakpoints as needed.

## (optional) Demonstrate the App

1. At a command line, change the current director to the one that contains "notebook.ipynb" (usually "nbtmpl").
1. If using conda, enter `conda activate nbtmpl`
1. Enter `jupyter-notebook &`
1. Click on the "notebook.ipynb" file.
1. Click on the "AppMode" button.

## "Access denied" Error

A browser window should appear when you run "jupyter-lab" or "jupyter-notebook". However, if the displayed page indicates access was denied, close the browser window and start another using one of the other URLs listed in the jupyter-lab/notebook output. Us a URL starting with "http://localhost...".

## (optional) Use composable infrastructure to host app

Currently, only the Docker container system is documented here. Additional container systems should be added later.

NOTE: The following steps pull the notebook code from a repository. If you've customized the template:
1. Create a git repository to host your code.
1. Commit your latest changes to that repo.
1. Substiture your repo's URL and name in "repourl=..." and "repodir=..." below.

### Build and test container

1. Install [Docker](https://docs.docker.com/get-docker/) on your workstation. Note that you may need admin access to run Docker commands.
1. Start a command line (terminal) session.
1. Make sure Docker is running by entering: [`docker info`](https://docs.docker.com/config/daemon/).
1. Build the Docker image by entering the following (note: final "`.`" is required.): `docker build -t nbtmpl1 --build-arg repourl=https://github.com/rcpurdue/nbtmpl.git .`
1. Run the image: `docker run -p 8866:8866 nbtmpl1`
1. Run the app (notebook) in your browser: `http://localhost:8866/`

NOTE: In the commands above:
 -  `nbtmpl1` = arbitrary name for the Docker image - use whatever you want
 -  `https://...` = repository URL - substitute your own when you customize the code
 -  `nbtmpl` = repo name (and, therefore, the name of the repo's directory) - change if customized
 -  `data` = relative path to the directory holding data files - change as needed
 -  `8866:8866` = connection port mapping within and out of container - change if needed

### Upload container

To allow others to run your app, it must be hosted on a publicly available Docker hosting system. There are a wide variety of options available including commercial sites like Amazon's AWS. Some institutions maintain their own Docker hosting systems. Depending on the specific reqirements of the hosting system you select, you'll need to provide either:
- a `Dockerfile` similar to one included in this repo, or
- a Docker image like the one built above.
You might be required to access the host system's Kubernetes management system (e.g. Rancher) to create the container and allocate resources.

## (optional) Development Using Container

An alternate Dockerfile is provided to facilitate development iterations (write code, test, repeat). In this scenario the container reaches out onto your workstation's filesystem to read the code and data. This allows you to make changes to the code or data and then just refresh the page in your browser to test it (rather than rebuilding the image). A separate development image is built and run below. Notice the special development Dockerfile that's used (`./dev/Dockerfile`):

1. Build the dev image: `docker build -t nbtmpl_dev1 dev/Dockerfile .`
1. Run the devimage: `docker run -p 8866:8866 --mount type=bind,src=/home/rcampbel/repos/nbtmpl,target=/home/jovyan/external nbtmpl_dev1`

NOTE: Change "`/home/rcampbel/repos/nbtmpl`" to the full path to your local repo.
