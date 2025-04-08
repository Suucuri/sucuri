#FROM python:3.12.9-slim-bookworm
FROM python:3.12.2-slim-bullseye
LABEL labase.author="carlo@ufrj.br"
LABEL version="25.04"
LABEL description="Suucuri - Learn Python with games"
COPY ./requirements.txt /etc
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -q -r /etc/requirements.txt
RUN mkdir -p /var/www/suucuri
ADD . /var/www/suucuri

# 👇
#ARG GIT_HASH
#ENV GIT_HASH=${GIT_HASH:-dev}
# 👆
RUN adduser --system labuser
USER labuser
EXPOSE 8665

WORKDIR /var/www/suucuri
#ENTRYPOINT ["top", "-b"]
ENTRYPOINT ["python3", "wsgi.py", "--port=8665", "--debug=True"]
#CMD ["python3", "wsgi.py", "--port=8575", "--debug=True"]
