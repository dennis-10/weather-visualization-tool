FROM python:3.8

WORKDIR /backend
COPY . .

RUN pip install -r requirements.txt

# ENTRYPOINT ["python"]
CMD ["uvicorn", "src.main:app", "--reload"]
EXPOSE 8080