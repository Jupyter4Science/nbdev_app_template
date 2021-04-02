FROM jupyter/scipy-notebook
RUN    conda install -c conda-forge 'voila'        \
    && conda install -c plotly      'plotly=4.5.0' \
    && conda clean --all -f -y                     \
    && mkdir external
WORKDIR external
CMD ["voila","--no-browser","loti.ipynb"]
