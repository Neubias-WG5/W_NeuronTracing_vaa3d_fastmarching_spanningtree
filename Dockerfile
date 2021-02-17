FROM python:3.6.9-stretch

# ---------------------------------------------------------------------------------------------------------------------
# Install Java, needed for Metric TreTrc using DIADEM.jar
RUN apt-get update && apt-get install openjdk-8-jdk -y && apt-get clean

# ---------------------------------------------------------------------------------------------------------------------
# Install Cytomine python client (annotation exporter, compute metrics, helpers,...)
RUN git clone https://github.com/cytomine-uliege/Cytomine-python-client.git && \
    cd /Cytomine-python-client && git checkout v2.7.3 && pip install . && \
    rm -r /Cytomine-python-client
    
# ---------------------------------------------------------------------------------------------------------------------
# Install Neubias-W5-Utilities (annotation exporter, compute metrics, helpers,...)    
# It will get DiademMetric.jar and JSAP-2.1.jar files to compute DIADEM metric
RUN apt-get update && apt-get install libgeos-dev -y && apt-get clean
RUN git clone https://github.com/Neubias-WG5/biaflows-utilities.git && \
    cd /biaflows-utilities/ && git checkout tags/v0.9.1 && pip install .

# install utilities binaries
RUN chmod +x /biaflows-utilities/bin/*
RUN cp /biaflows-utilities/bin/* /usr/bin/

# cleaning
RUN rm -r /biaflows-utilities    


# --------------------------------------------------------------------------------------------
# install required packages and download vaa3d
RUN wget https://github.com/Vaa3D/release/releases/download/v3.458/Vaa3D_CentOS_64bit_v3.458.tar.gz --directory-prefix=/
RUN tar -xvzf Vaa3D_CentOS_64bit_v3.458.tar.gz
RUN apt-get update
RUN apt-get install -y \
        libqt4-svg \
        libqt4-opengl \
        libqt4-network \
        libglu1-mesa
RUN apt-get install -y curl xvfb libx11-dev libxtst-dev libxrender-dev

# --------------------------------------------------------------------------------------------
# Install scripts and models
ADD wrapper.py /app/wrapper.py
ADD workflow.py /app/workflow.py
ADD swc_to_tiff_stack.py /app/swc_to_tiff_stack.py
ADD descriptor.json /app/descriptor.json

ENTRYPOINT ["python", "/app/wrapper.py"]


