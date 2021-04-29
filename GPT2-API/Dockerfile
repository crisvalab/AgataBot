FROM tensorflow/tensorflow:1.15.0-gpu-py3

# nvidia-docker 1.0
LABEL com.nvidia.volumes.needed="nvidia_driver"
LABEL com.nvidia.cuda.version="${CUDA_VERSION}"

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility \
    NVIDIA_REQUIRE_CUDA="cuda>=8.0" \
    LANG=C.UTF-8

WORKDIR /app

COPY . /app

RUN python -m pip install pip==21.0.1
RUN pip install -r requirements.txt

CMD ["python", "apiservice.py"]

#sudo docker run --runtime=nvidia -it gptapi