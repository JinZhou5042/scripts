python test.py

dir="vine-run-info/most-recent/vine-logs"
python new_plot.py ${dir}/transactions ${dir}/txn

rsync -avP ${dir}/txn 10.2.17.65:/Users/jinzhou/Downloads

