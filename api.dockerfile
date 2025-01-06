FROM python:3.10
WORKDIR /code
COPY ./api.tar /code
RUN tar xf api.tar
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --no-cache-dir --upgrade -r /code/requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
