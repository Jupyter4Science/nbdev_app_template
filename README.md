# nbtmpl - Notebook Template
A Python code template for building web apps without writing HTML, CSS. and JavaScript.

<table><tr><td width="14%">
    <img src="https://www.python.org/static/img/python-logo.png" alt="python logo">
    </td><td width="14%">
    <img src="https://pandas.pydata.org/static/img/pandas_white.svg" alt="pandas logo">
    </td><td width="14%">
    <img src="https://matplotlib.org/_static/images/logo2.svg" alt="matplotlib logo">
    </td><td width="14%">
    <b>ipywidgets</b>
    </td><td width="14%">
    <img src="https://jupyter.org/assets/nav_logo.svg" alt="jupyter logo">
    </td><td width="10%">
    <img src="https://raw.githubusercontent.com/voila-dashboards/voila/main/docs/source/voila-logo.svg" alt="voila logo">
    </td><td width="14%">
    <img src="https://www.docker.com/sites/default/files/d8/styles/role_icon/public/2019-07/horizontal-logo-monochromatic-white.png" alt="docker logo">
</td></tr></table>

Got a Python project or Jupyter notebook? Want to turn into a web applilcation?

This repository contains example code, written in [Python](https://www.python.org/), that you can easily modify. It can act as a template to show how you can use [ipywidgets](https://ipywidgets.readthedocs.io/en/stable/) to build an interactive web application. It relies on [Jupyter](https://jupyter.org/) notebook infrasturcture. However, the app looks like a web app - not a notebook. Further, it demonstrates the use of [Docker](https://www.docker.com/) and [Voilà](https://github.com/voila-dashboards/voila) to allow the app to be hosted on composable infrastructure. The example code uses [pandas](https://pandas.pydata.org/) for data access and [Matplotlib](https://matplotlib.org/) to generate plots.

The template was developed so researchers can quickly and easily put their project on the web without getting bogged down in conventional web developement (AJAX, HTML, CSS, JS, etc.). The example notebook uses global temperature data from NASA to show how users can view, search, download, and plot data using an interactive, web enabled tool.

## How It Works

Source code is organized in a loose [Model-view-controller](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller) pattern. The code is divided into three classes in the "nb" directory:

- Model: Works with storage (file system, database, etc)
- View:  Builds the user interface (widgets, plots, etc.)
- Controller: Responds to user actions (button presses, menu selections, etc.)

The Jupyter notebook ('notebook.ipynb") contains just one code cell. This kicks of the model/view/controler code and the web app starts running.

The code relies on [widgets](https://en.wikipedia.org/wiki/Graphical_widget) and [callbacks](https://en.wikipedia.org/wiki/Callback_(computer_programming)) methods. Once its up and running, the code waits for the user to make changes to user interface widgets. But widget updates also work in both directions. When the user interacts with a widget in their browser, an assigned callback method runs. And when some code changes a widget, those changes appear in the browser.

For example, the view object creates a button named "filter_btn_apply". The controller specifies that, when this button is pressed, its "cb_apply_filter()" method is called ("view.filter_btn_apply.on_click(self.cb_apply_filter)"). The "cb_apply_filter()" method then directs the model to perform the query and then the view to update the output widget ("output()" updates self.filter_output).

## Developing and testing on your workstation

The template requires Python, Jupyter, and a number of Python packages. Follow the steps below to ensure all dependencies are installed and configured propery. The Andaconda package management system is used to create an environment for running the notebook. Anaconda's `conda` command will be used to automatically install required packages and their dependecies.

### Create the conda environment (one time only)
1. Install [Anaconda](https://www.anaconda.com/products/individual) on your system.
1. At the OS command line, run: `conda env create --file environment.yml`. This creates a conda environment called "nbtmpl" and installs software modules. Answer "y" to prompts.

### Activate the conda environment
1. Next, enter `conda activate nbtmpl`. This changes your current command line environemnt so the code has access to required software packages. You should see `(nbtmpl)` at the beginning of your command line prompt.
1. NOTE: You'll need to run this command _every time you start up Jupyter to develop and test your code_.

### Start Jupyter and run the notebook
1. At a command line, enter `conda activate nbtmpl`
1. Enter `jupyter lab`. (See [Starting JupyterLab](https://jupyterlab.readthedocs.io/en/stable/getting_started/starting.html) for more info.
1. Browse to the nbtmpl directory and double click on the `notebook.ipynb` file.
1. Click the "Restart kernel...re-run...notebook" button (double trinangle icon).
1. When prompted, click the "Restart" button.
1. NOTE: Later, when the notebook and code runs as a web app, only the title, tabs, and tab content will appear. The Jupyter Lab UI and the notebook's code cell will not appear.

### Debugging
For simple bugs, use the log and [print debugging](https://en.wikipedia.org/wiki/Debugging#Techniques) (`logger.debug(...)`) to display values of variables. The log can viewed in Jupyter Lab's "Log Console" (menu: View --> Show Log Console). Set "Log Level" to
"Debug". For more difficult bugs, use Jupyter Lab's [debugger](https://jupyterlab.readthedocs.io/en/stable/user/debugger.html). Set a breakpoint in the line of code in the notebook (after the import). Using the debugger, run to that breakpoing. Then, step into the mvc code and set more breakpoints as needed.

## Demonstrating the web app on your workstation

1. At a command line, change the current director to the one that contains "notebook.ipynb" (usually "nbtmpl").
1. Enter `conda activate nbtmpl`
1. `jupyter-notebook &`
1. Click on the "notebook.ipynb" file.
1. Click on the "AppMode" button.

## Access denied error

A browser window should appear when you run "jupyter-lab" or "jupyter-notebook". However, if the displayed page indicates access was denied, close the browser window and start another using one of the other URLs listed in the jupyter-lab/notebook output. Us a URL that starting with "http://localhost...".


## Using composable infrastructure to host your web app

## Running in a Docker Container

### Install Docker application

#### On MacOS systems
Install Docker application from the Docker website https://hub.docker.com/editions/community/docker-ce-desktop-mac/. Click blue box with 'Get Docker' text. This will download a Docker.dmg file. Upon opening the disk image (.dmg) file, you will be asked to drag the Docker App icon into your Applications.
Go to your Applications folder and double click 'Docker' to open the program. Once you see a whale image in your upper bar, Docker is running. You may now close the pop-up window, Docker will continue to run in the background.

#### On Debian-based Linux systems
As root (sudo), enter...
```
apt install docker.io
```

### Build Docker image

Run the build step:

```
docker build -t <image_name> --build-arg repourl=<repository_url> --build-arg repodir=<repository_name> --build-arg repodir=<datapath> <path_to_data_files> <path_to_dockerfile>
```

For example, the code I ran was:

```
docker build -t nbtmpl1 --build-arg repourl=https://github.com/rcpurdue/nbtmpl.git --build-arg repodir=nbtmpl --build-arg datapath=data .
```
...where:

 -  "`nbtmpl1`" is an arbitrary name we will use to identify the image that will be created.
 -  "`https://...`" is URL for this repository.
 -  "`nbtmpl`" is the name of this repository (and, therefore, the name of the repo's directory).
 -  "`data`" is the local path to the directory holding the data files.

**Note 1:** The latest version of the code is pulled down from the repository. Make sure to commit your local changes first.

**Note 2:** This step will take several minutes.

### Run the image.
```
docker run -p 8866:8866 <image_name>
```

...where `8866` is the network connection port

For example:

```
docker run -p 8866:8866 nbtmpl1

```

### Run the notebook (via browser)

```
http://localhost:8866/
```

## Developing Using a Docker Container - "Dev Mode"

An alternate Dockerfile is provided to facilitate development iterations (writing code, testing, repeating) while stil leveraging Docker.
In this scenario, the site still runs within the Docker image, however it reaches out onto the host filesystem to read the code and data.
This allows you to make changes to the code or data and then just refresh the page in your browser to test it (rather than rebuilding the image).

The image is built using the following command. Note that the path to the special development Dockerfile should be used (e.g. "./dev/Dockerfile").

```
docker build -t <dev_image_name> <path_to_dev_dockerfile>
```

Use this command to run the "dev mode" docker image:

```
docker run -p 8866:8866 --mount type=bind,src=<full_path_to_repo>,target=/home/jovyan/external <dev_image_name>
```
