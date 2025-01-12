FROM ubuntu:20.04

ARG USERNAME=moshpp
ARG GROUPNAME=${USERNAME}
ARG USER_PASS=${USERNAME}
ARG UID=1000
ARG GID=${UID}

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    SHELL=/bin/bash

USER root
RUN apt-get update && apt-get install -y \
    sudo \
    git wget curl \
    build-essential \
    nfs-common cifs-utils rpcbind \
    libatlas-base-dev \
    libpython3.7 \
    libtbb2 libtbb-dev \
    libeigen3-dev \
    libboost-dev \
    python3-opengl \
    libxrender1 libfftw3-3 libpng16-16 libjpeg-turbo8 libtiff5 libopenjp2-7 libfreetype6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -g ${GID} ${GROUPNAME} \
    && useradd -m -s /bin/bash -u ${UID} -g ${GID} ${USERNAME} \
    && gpasswd -a ${USERNAME} sudo \
    && echo "${USERNAME}:${USER_PASS}" | chpasswd

USER ${USERNAME}
ENV HOME=/home/${USERNAME}
ENV PATH=${PATH}:${HOME}/.local/bin
WORKDIR ${HOME}

RUN mkdir -p ~/miniconda3 \
    && wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh \
    && bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3 \
    && rm ~/miniconda3/miniconda.sh
ENV PATH=${HOME}/miniconda3/bin:${PATH}

RUN conda create -n moshpp python==3.7 \
    && echo "source activate moshpp" >> ~/.bashrc
SHELL ["conda", "run", "-n", "moshpp", "/bin/bash", "-c"]

RUN pip install --upgrade pip \
    && conda install -c conda-forge ezc3d \
    && pip install torch==1.8.2 torchvision==0.9.2 torchaudio==0.8.2 --extra-index-url https://download.pytorch.org/whl/lts/1.8/cpu

RUN git clone https://github.com/nghorbani/soma.git \
    && cd soma \
    && pip install -r requirements.txt \
    && python setup.py develop

RUN git clone https://github.com/MPI-IS/mesh.git \
    && cd mesh \
    && python setup.py install

RUN git clone https://github.com/nghorbani/moshpp.git \
    && cd moshpp \
    && sed 's/^sklearn$/scikit-learn/I' requirements.txt | pip install -r /dev/stdin \
    && pip install -r src/moshpp/scan2mesh/requirements.txt \
    && make -C src/moshpp/scan2mesh/mesh_distance \
    && python setup.py install

COPY ./downloads .
COPY ./run_moshpp.py .

CMD [ "bash" ]