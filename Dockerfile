# xhost +  ! remember to disable access control by executing 'xhost -' !
# sudo docker run -it --net=host --env="DISPLAY" --volume="$HOME/.Xauthority:/root/.Xauthority:rw" <image_name/id>

FROM python

ADD krypto.py .
ADD requirements.txt .

RUN pip install -r requirements.txt

CMD [ "python", "krypto.py", "3" ]
