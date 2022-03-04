FROM jupyter/scipy-notebook

# install packages we need for deploying the standalone app with Voila
RUN mamba install -c conda-forge voila jupyterthemes

# packages we need for interactive literate programming
RUN mamba install -c fastai nbdev

# install any user packages defined in environment.yml
WORKDIR "/home/${NB_USER}/work"
COPY environment.yml .
RUN mamba env update --file environment.yml
