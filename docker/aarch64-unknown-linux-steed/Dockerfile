FROM ubuntu:16.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    gcc \
    libc6-dev && \
    mkdir /json

COPY qemu.sh /
RUN apt-get install -y --no-install-recommends \
    gcc-aarch64-linux-gnu && \
    bash /qemu.sh 2.8.0 aarch64

COPY aarch64-unknown-linux-steed.json /json

RUN apt-get install -y --no-install-recommends \
    curl && \
    curl -LSfs http://japaric.github.io/trust/install.sh | \
    sh -s -- --git japaric/xargo --tag v0.3.5 --target x86_64-unknown-linux-gnu --to /usr/bin && \
    apt-get purge --auto-remove -y curl

ENV CARGO_TARGET_AARCH64_UNKNOWN_LINUX_STEED_LINKER=aarch64-linux-gnu-gcc \
    RUST_TARGET_PATH=/json \
    RUST_TEST_THREADS=1
