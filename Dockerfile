FROM python:3.10

ARG CHROME_VERSION="118.0.5993.70-1"
RUN wget -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}_amd64.deb
RUN apt-get -y update
RUN apt-get install -y /tmp/chrome.deb
#
RUN apt-get install -yqq unzip
RUN wget --no-check-certificate -O /tmp/chromedriver.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/118.0.5993.70/linux64/chromedriver-linux64.zip
RUN unzip /tmp/chromedriver.zip -d /tmp/
RUN cp /tmp/chromedriver-linux64/chromedriver /usr/local/bin/

RUN apt-get install -y vim

RUN pip install --upgrade pip
RUN pip install selenium boto3

WORKDIR /scratch/BTS_Referance_Data/
COPY bts_reference_data_scraper.py .


CMD ["python", "./bts_reference_data_scraper.py"]
ENTRYPOINT ["tail", "-f", "/dev/null"]

#RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
#RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
##
#RUN apt-get -y update
#RUN apt-get install -y google-chrome-stable
##
#RUN apt-get install -yqq unzip
#RUN wget --no-check-certificate -O /tmp/chromedriver.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/118.0.5993.70/linux64/chromedriver-linux64.zip
#RUN unzip /tmp/chromedriver.zip -d /tmp/
#RUN cp /tmp/chromedriver-linux64/chromedriver /usr/bin/chromedriver

#RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | \
#    tee -a /etc/apt/sources.list.d/google.list && \
#    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | \
#    apt-key add - && \
#    apt-get update && \
#    apt-get install -y google-chrome-stable libxss1
#
#RUN BROWSER_MAJOR=$(google-chrome --version | sed 's/Google Chrome \([0-9]*\).*/\1/g') && \
#    wget https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${BROWSER_MAJOR} -O chrome_version && \
#    wget https://chromedriver.storage.googleapis.com/`cat chrome_version`/chromedriver_linux64.zip && \
#    unzip chromedriver_linux64.zip && \
#    mv chromedriver /usr/local/bin/ && \
#    DRIVER_MAJOR=$(chromedriver --version | sed 's/ChromeDriver \([0-9]*\).*/\1/g') && \
#    echo "chrome version: $BROWSER_MAJOR" && \
#    echo "chromedriver version: $DRIVER_MAJOR" && \
#    if [ $BROWSER_MAJOR != $DRIVER_MAJOR ]; then echo "VERSION MISMATCH"; exit 1; fi
#RUN apt-get install -yqq unzip
#RUN wget --no-check-certificate -O /tmp/chromedriver.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/118.0.5993.70/linux64/chromedriver-linux64.zip
#RUN unzip /tmp/chromedriver.zip -d /tmp/
#RUN cp /tmp/chromedriver-linux64/chromedriver /usr/local/bin/



#WORKDIR /tmp/
#RUN apt update
#RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#RUN apt install ./google-chrome-stable_current_amd64.deb
#
#RUN wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/118.0.5993.70/linux64/chromedriver-linux64.zip
#RUN unzip chromedriver-linux64.zip
#RUN mv /tmp/chromedriver-linux64/chromedriver /usr/bin/chromedriver

#RUN useradd -ms /bin/bash newuser
#USER newuser

#WORKDIR /scratch/BTS_Referance_Data/
#COPY bts_reference_data_scraper.py .


#CMD ["python", "./bts_reference_data_scraper.py"]
#ENTRYPOINT ["tail", "-f", "/dev/null"]