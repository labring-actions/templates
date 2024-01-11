FROM bitnami/git
WORKDIR /data
RUN git clone https://github.com/labring-actions/templates.git --depth=1
CMD ["sh", "-c", "ls -a /data/templates"]