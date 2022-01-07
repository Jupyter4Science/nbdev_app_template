FROM jupyter/scipy-notebook
ARG repourl
RUN conda install -c conda-forge voila jupyterthemes \
    && git clone --depth 1 $repourl target
WORKDIR /home/jovyan/target
# CMD ["bash"]
# CMD ["jupyter-notebook","--port=8866"]
CMD ["voila","notebook.ipynb","--no-browser","--Voila.ip","0.0.0.0"]
