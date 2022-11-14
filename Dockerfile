FROM python:3.10
ADD . /stori_card_assessment
WORKDIR /stori_card_assessment
RUN pip install -r requirements.txt