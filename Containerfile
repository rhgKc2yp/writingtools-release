FROM registry.fedoraproject.org/fedora:45

# Use a Python version supported by the upstream Qt wheels.
RUN dnf install -y python3.13 python3.13-devel gcc binutils git tar gzip \
    mesa-libGL mesa-libEGL libxkbcommon-x11 xcb-util-cursor xcb-util-wm xcb-util-image \
    xcb-util-keysyms xcb-util-renderutil libX11 libXext libXrender libXi \
    fontconfig freetype dbus-libs xclip xorg-x11-server-Xvfb xorg-x11-xauth \
    && dnf clean all

WORKDIR /build
ARG UPSTREAM_REF
RUN test -n "$UPSTREAM_REF" \
    && git init source \
    && git -C source remote add origin https://github.com/theJayTea/WritingTools.git \
    && git -C source fetch --depth=1 origin "$UPSTREAM_REF" \
    && git -C source checkout --detach FETCH_HEAD \
    && git -C source rev-parse HEAD > /build/upstream-commit.txt

RUN python3.13 -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
RUN python -m pip install --upgrade pip \
    && python -m pip install -r source/Windows_and_Linux/requirements.txt \
    && python -m pip check

COPY scripts/build-in-container.sh scripts/smoke-hook.py /build/scripts/
RUN bash /build/scripts/build-in-container.sh
CMD ["bash", "-c", "cp -a /artifacts/. /output/"]
