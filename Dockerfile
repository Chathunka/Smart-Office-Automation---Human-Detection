FROM python:3.9-slim-buster

WORKDIR /app
# Copy the main script file to the container
COPY main.py /app/

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get update && apt-get -y install git libgl1-mesa-glx

RUN apt-get update && apt-get install -y libglib2.0-0

RUN python -m pip install torch==1.9.0 -f https://download.pytorch.org/whl/torch_stable.html
# update apt and install git
RUN apt-get update && apt-get -y install git

RUN apt-get update \
    && apt-get install -y python3-dev gcc \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

RUN git clone https://github.com/ultralytics/yolov5 && \
    cd yolov5 && \
    pip install -r https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt

CMD [ "python", "main.py" ]
