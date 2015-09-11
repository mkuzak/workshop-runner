FROM python:2.7
ADD ./requirements.txt /requirements.txt
RUN pip install /requirements.txt
WORKDIR /ipsheet
ENTRYPOINT ["python", "/ipsheet/ipsheet.py"]
