FROM python:3.11-slim
WORKDIR /app/srec
COPY srec ./srec
RUN pip install --no-cache-dir -r srec/requirements.txt
CMD ["python","-m","srec.compiler","."]