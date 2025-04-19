ARG AIRFLOW_UID=50000
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

# ENV JAVA_HOME=/home/jdk-11.0.2

# ENV PATH="${JAVA_HOME}/bin/:${PATH}"

# RUN DOWNLOAD_URL="https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz" \
#     && TMP_DIR="$(mktemp -d)" \
#     && curl -fL "${DOWNLOAD_URL}" --output "${TMP_DIR}/openjdk-11.0.2_linux-x64_bin.tar.gz" \
#     && mkdir -p "${JAVA_HOME}" \
#     && tar xzf "${TMP_DIR}/openjdk-11.0.2_linux-x64_bin.tar.gz" -C "${JAVA_HOME}" --strip-components=1 \
#     && rm -rf "${TMP_DIR}" \
#     && java --version

USER root

# Cài openjdk-11 từ nguồn bullseye (ổn định hơn bookworm trên ARM)
# RUN echo "deb http://deb.debian.org/debian bullseye main" >> /etc/apt/sources.list && \
#     apt-get update && \
#     apt-get install -y openjdk-11-jdk && \
#     rm -rf /var/lib/apt/lists/*

# ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
# ENV PATH="$JAVA_HOME/bin:$PATH"

# RUN java -version

USER root

# Thêm nguồn ổn định từ bullseye
RUN echo "deb http://deb.debian.org/debian bullseye main" >> /etc/apt/sources.list && \
    apt-get update && \
    if [ "$(dpkg --print-architecture)" = "amd64" ]; then \
        apt-get install -y openjdk-11-jdk && \
        export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64 ; \
    else \
        apt-get install -y openjdk-11-jdk && \
        export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64 ; \
    fi && \
    rm -rf /var/lib/apt/lists/* && \
    echo "JAVA_HOME=$JAVA_HOME" && \
    java -version

# Đặt JAVA_HOME mặc định (sẽ tương ứng nếu container build đúng)
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
ENV PATH="$JAVA_HOME/bin:$PATH"

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
