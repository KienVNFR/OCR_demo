FROM pytorch/pytorch:1.9.0-cuda10.2-cudnn7-devel
COPY . /workspace/OCR_demo
WORKDIR /workspace/OCR_demo
#RUN pip install -r requirements.txt

#RUN chmod +x run.sh 
#RUN ./run.sh 
