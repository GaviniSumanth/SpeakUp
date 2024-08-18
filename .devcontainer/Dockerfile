FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    bash \
    bash-completion \
    nano \
    python3-virtualenv \
    sudo \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* \
    && hash -r

WORKDIR /workspace

ARG USERNAME=appuser
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --create-home --uid $USER_UID --gid $USER_GID $USERNAME -s /bin/bash \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

RUN mkdir -p /var/log/speakup
RUN chown -R $USERNAME:$USERNAME /var/log/speakup
USER $USERNAME
