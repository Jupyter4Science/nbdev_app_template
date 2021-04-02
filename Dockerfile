FROM jupyter/scipy-notebook
ARG repourl
ARG repodir
ARG datapath
RUN    conda install -c conda-forge 'voila'        \
    && conda install -c plotly      'plotly=4.5.0' \
    && conda clean --all -f -y                     \
    && git clone --depth 1 $repourl                \
    && mkdir $repodir/data
COPY --chown=jovyan:users $datapath $repodir/data
WORKDIR $repodir
CMD ["voila","--no-browser","loti.ipynb"]
