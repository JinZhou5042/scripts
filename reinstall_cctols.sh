cd ~/cctools
make clean
if [[ $1 == "--conda" ]]; then
	./configure --with-base-dir $CONDA_PREFIX --prefix $CONDA_PREFIX
elif [[ $1 == "--cctools" ]]; then
        ./configure --prefix $HOME/cctools
else
        exit 1 
fi

make -j8
make install
