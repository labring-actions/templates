FROM bitnami/git
WORKDIR /data
RUN git clone https://github.com/labring-actions/templates.git
CMD ["sh", "-c", "ls -a /data/templates"]