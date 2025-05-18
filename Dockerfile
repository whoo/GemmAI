FROM alpine
RUN apk add py3-pip ; \
    adduser -D py ; \
    mkdir /GemmAI; \
    chown -R py: /GemmAI

USER py
ENV PATH=$PATH:/home/py/.local/bin
ADD /GemmAI /GemmAI/GemmAI
RUN mkdir /GemmAI/db
WORKDIR /GemmAI/GemmAI
RUN pip install -r  requirements.txt --break-system-packages
RUN flask db upgrade
ENV API=''
ENV NAME='GemmAI'
CMD ["gunicorn", "app:app" ]

