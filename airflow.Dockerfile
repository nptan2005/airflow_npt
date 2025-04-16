ARG AIRFLOW_IMAGE_NAME
FROM ${AIRFLOW_IMAGE_NAME}

ENV AIRFLOW_HOME=/opt/airflow

WORKDIR $AIRFLOW_HOME

# USER root
# RUN apt-get update -qq && apt-get install vim -qqq && apt-get install -y python3-pip

# Cài đặt các gói cần thiết, bao gồm pg_config
USER root
RUN apt-get update \
    && apt-get install vim -qqq  \
    && apt-get install -y python3-pip \
    && apt-get install -y --no-install-recommends libpq-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/home/jdk-11.0.2

ENV PATH="${JAVA_HOME}/bin/:${PATH}"

RUN DOWNLOAD_URL="https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz" \
    && TMP_DIR="$(mktemp -d)" \
    && curl -fL "${DOWNLOAD_URL}" --output "${TMP_DIR}/openjdk-11.0.2_linux-x64_bin.tar.gz" \
    && mkdir -p "${JAVA_HOME}" \
    && tar xzf "${TMP_DIR}/openjdk-11.0.2_linux-x64_bin.tar.gz" -C "${JAVA_HOME}" --strip-components=1 \
    && rm -rf "${TMP_DIR}" \
    && java --version

# Thêm Oracle Instant Client
USER root
RUN apt-get update && apt-get install -y wget unzip libaio1 \
    && wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basic-linuxx64.zip \
    && unzip instantclient-basic-linuxx64.zip -d /opt/oracle \
    && rm -f instantclient-basic-linuxx64.zip


ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_21_1:$LD_LIBRARY_PATH
ENV ORACLE_HOME=/opt/oracle/instantclient_21_1

# Cài đặt Poetry
# Cài đặt Poetry và thiết lập $PATH
# RUN curl -sSL https://install.python-poetry.org | python3 - \
#     && ln -s /root/.local/bin/poetry /usr/local/bin/poetry
# RUN echo $PATH && poetry --version



USER airflow
COPY airflow.requirements.txt .
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r airflow.requirements.txt
# Cài đặt thư viện PostgreSQL provider
# RUN pip install apache-airflow-providers-postgres

USER root
COPY scripts scripts
RUN chmod +x scripts

USER $AIRFLOW_UID
