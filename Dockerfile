# Image de base
FROM python:3.8.5-alpine3.12 as base
RUN apk update && apk add bash
RUN apk add curl
RUN apk add --update build-base

FROM base
COPY src /referencedata
WORKDIR /referencedata/
RUN pip install -r requirements.txt

EXPOSE 8000
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
