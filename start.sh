#!/bin/bash


docker run -d -it --name dslab_nlp_container --gpus '"device=1"' -v $(pwd):/workspace -p 5000:5000 kwanhoon/dslab_nlp
