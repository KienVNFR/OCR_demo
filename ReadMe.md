# build docker 
    sudo docker build -t ocr-demo:1.1 . 
# run docker img 
    sudo docker run -it --name ocr_demo ocr-demo:1.1 bash 
# ad run.sh 
   chmod +x run.sh 
# run run.sh 
   ./run.sh 
# run file demo 
 python3 demo -- 
