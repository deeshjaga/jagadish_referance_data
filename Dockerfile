FROM debian:buster-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y --no-install-recommends firefox-esr && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


RUN mkdir -p /downloads
ENV DOWNLOAD_PATH /downloads

RUN pip3 install selenium==3.141.0
RUN pip3 install --upgrade urllib3==1.26.16
RUN pip3 install boto3


RUN apt-get update && \
    apt-get install -y wget && \
    wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz && \
    tar -xvzf geckodriver-v0.34.0-linux64.tar.gz && \
    chmod +x geckodriver && \
    mv geckodriver /usr/local/bin/ && \
    rm geckodriver-v0.34.0-linux64.tar.gz && \
    apt-get purge -y wget && \
    apt-get autoremove -y


WORKDIR /scratch/BTS_Referance_Data/
COPY bts_reference_data_scraper.py .


CMD ["python", "./bts_reference_data_scraper.py"]
ENTRYPOINT ["tail", "-f", "/dev/null"]

