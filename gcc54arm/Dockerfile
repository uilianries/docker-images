FROM lasote/conangcc54:latest

LABEL maintainer="Uilian Ries <uilianries@gmail.com>"

ENV PATH="${PATH}:/opt/gcc-linaro/bin" \
    CC=arm-linux-gnueabihf-gcc \
    CXX=arm-linux-gnueabihf-g++ \
    SYSROOT=/opt/sysroot

RUN wget -q -O /tmp/libssl-dev_1.0.2g-1ubuntu4.9_armhf.deb http://launchpadlibrarian.net/344119130/libssl-dev_1.0.2g-1ubuntu4.9_armhf.deb \
    && dpkg-deb -x /tmp/libssl-dev_1.0.2g-1ubuntu4.9_armhf.deb /tmp/libssl-dev \
    && sudo mkdir -p /opt/openssl/lib \
    && sudo mv /tmp/libssl-dev/usr/include /opt/openssl \
    && sudo mv /opt/openssl/include/arm-linux-gnueabihf/openssl/opensslconf.h /opt/openssl/include/openssl/opensslconf.h \
    && sudo cp /tmp/libssl-dev/usr/lib/arm-linux-gnueabihf/*.a /opt/openssl/lib \
    && wget -q -O /tmp/libssl1.0.0_1.0.2g-1ubuntu4.9_armhf.deb http://launchpadlibrarian.net/344119132/libssl1.0.0_1.0.2g-1ubuntu4.9_armhf.deb \
    && dpkg-deb -x /tmp/libssl1.0.0_1.0.2g-1ubuntu4.9_armhf.deb /tmp/libssl1 \
    && sudo cp /tmp/libssl1/lib/arm-linux-gnueabihf/libcrypto.so.1.0.0 /opt/openssl/lib/libcrypto.so \
    && sudo cp /tmp/libssl1/lib/arm-linux-gnueabihf/libssl.so.1.0.0 /opt/openssl/lib/libssl.so \
    && wget -q -O /tmp/sysroot-glibc-linaro-2.21-2017.05-arm-linux-gnueabihf.tar.xz http://releases.linaro.org/components/toolchain/binaries/5.4-2017.05/arm-linux-gnueabihf/sysroot-glibc-linaro-2.21-2017.05-arm-linux-gnueabihf.tar.xz \
    && tar Jxf /tmp/sysroot-glibc-linaro-2.21-2017.05-arm-linux-gnueabihf.tar.xz -C /tmp \
    && sudo mv /tmp/sysroot-glibc-linaro-2.21-2017.05-arm-linux-gnueabihf /opt/sysroot \
    && wget -q -O /tmp/gcc-linaro-5.4.1-2017.05-x86_64_arm-linux-gnueabihf.tar.xz http://releases.linaro.org/components/toolchain/binaries/5.4-2017.05/arm-linux-gnueabihf/gcc-linaro-5.4.1-2017.05-x86_64_arm-linux-gnueabihf.tar.xz \
    && tar Jxf /tmp/gcc-linaro-5.4.1-2017.05-x86_64_arm-linux-gnueabihf.tar.xz -C /tmp \
    && sudo mv /tmp/gcc-linaro-5.4.1-2017.05-x86_64_arm-linux-gnueabihf /opt/gcc-linaro \
    && rm -rf /tmp/*
