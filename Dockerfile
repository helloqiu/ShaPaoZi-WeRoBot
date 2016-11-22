FROM python:3.5.2-slim

COPY . /requirements/

WORKDIR /requirements/

RUN set -x \
    && echo "Asia/Shanghai" > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata \
    && rm /etc/apt/sources.list \
    && echo "deb http://mirrors.tuna.tsinghua.edu.cn/debian jessie main \n\
deb http://mirrors.tuna.tsinghua.edu.cn/debian jessie-updates main \n\
deb http://mirrors.tuna.tsinghua.edu.cn/debian-security/ jessie/updates main" >> /etc/apt/sources.list \
    && cat /etc/apt/sources.list \
    && apt-get update \
    && apt-get install gcc build-essential libssl-dev libffi-dev python-dev git -y \
    && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -U pip setuptools \
    && git clone https://github.com/whtsky/WeRoBot --depth=1 \
    && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt \
    && cd WeRoBot \
    && python setup.py install \
    && cd .. \
    && find /usr/local -type f -name '*.pyc' -name '*.pyo' -delete \
    && rm -rf ~/.cache/ \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*