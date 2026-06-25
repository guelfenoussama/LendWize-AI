# Base image.
FROM python:3.13-slim

RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --system --deploy
RUN pip install waitress streamlit
COPY . /app


EXPOSE 9697
EXPOSE 8501



CMD python FINAL_PROGECT_predict.py & streamlit run app_streamlit.py --server.port 8501 --server.address 0.0.0.0
