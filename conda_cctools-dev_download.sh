unset PYTHONPATH
conda create -y -n cctools-dev -c conda-forge --strict-channel-priority python=3 gcc_linux-64 gxx_linux-64 gdb m4 perl swig make zlib libopenssl-static openssl conda-pack packaging cloudpickle flake8 clang-format
conda activate cctools-dev
conda install -y numpy scipy pandas matplotlib tqdm scikit-learn
conda install -y conda-forge::psutil
