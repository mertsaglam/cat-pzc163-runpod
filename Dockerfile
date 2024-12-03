FROM python:3.10.12-slim

ENV DEBIAN_FRONTEND=noninteractive \
    NVIDIA_DRIVER_CAPABILITIES=all \
    PIP_PREFER_BINARY=1 \
    PYTHONUNBUFFERED=1

# Setup system packages
COPY builder/setup.sh /setup.sh
RUN /bin/bash /setup.sh && \
    rm /setup.sh

COPY builder/requirements.txt /requirements.txt 
RUN pip install -r /requirements.txt && \
    rm /requirements.txt

# Install ComfyUI
RUN git clone https://github.com/comfyanonymous/ComfyUI.git

WORKDIR /ComfyUI

RUN pip install -r requirements.txt && pip cache purge

# Clone custom Nodes
RUN git -C ./custom_nodes clone --depth 1 https://github.com/mertsaglam/Comfyui-CatVTON
#load requirements of the package
RUN pip install -r ./custom_nodes/Comfyui-CatVTON/requirements.txt
##go to main folder and load densepose and detectron2

RUN pip install git+https://github.com/facebookresearch/detectron2.git@v0.6
RUN pip install git+https://github.com/facebookresearch/detectron2.git@v0.6#subdirectory=projects/DensePose

# Custom nodes requirements
COPY --chmod=755 src/* ./
RUN ./install_custom_node_dependencies.sh
RUN pip install huggingface_hub==0.25.2 matplotlib


CMD /ComfyUI/start.sh