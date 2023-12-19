#!/bin/bash

help_info="
Usage: bash $0 [-opt]
opt:
	-h                   print help information
	-p  <port>           the working port
	-qc <query_count>    the number of queries for each task
	-tc <task_count>     the number of taskGs in total
	-wc <worker_count>   the number of workers
	-txn                 plot txn figure
	-worker              plot worker performance
	-xlsx                convert pfm log to xlsx
	-norun               don't run blast, do plot or convert only
example:
	bash $0 -p 9123 -tc 10000 -qc 20 -worker -txn
"

cctools_base="/afs/crc.nd.edu/user/j/jzhou24/cctools/"
# blast="${cctools_base}taskvine/src/examples/vine_example_blast.py"
blast="mytools/my_vine_example_blast.py"

vine_logs_base="/afs/crc.nd.edu/user/j/jzhou24/scripts/vine-run-info/most-recent/vine-logs/"
transactions_log="${vine_logs_base}transactions"
performance_log="${vine_logs_base}performance"

qc=2
port=9123
tc=10


while [[ "$#" -gt 0 ]]; do
	case $1 in
		-h)
			printf "%s\n" "$help_info"
			shift
			exit 0
			;;		
		-p)
			port="$2"
			shift 2
			;;
		-qc)
			qc="$2"
			shift 2
			;;
		-tc)
			tc="$2"
			shift 2
			;;
		-name)
			name="$2"
			shift 2
			;;
		-wc)
			wc="$2"
			shift 2
			;;
		-txn)
			taskvine_tools_base="${cctools_base}taskvine/src/tools/"
			opt_png="${vine_logs_base}txn_figure.png"
			txn_plot="${taskvine_tools_base}vine_plot_txn_log"
			txn=1
			shift 1
			;;
		-worker)
			wkpfm_plot="mytools/vine_worker_performance.py"
			worker=1
			shift 1
			;;
		-xlsx)
			convert="mytools/convert_log_performance_to_xlsx.py"
			xlsx=1
			shift 1
			;;
		-norun)
			norun=1
			shift 1
			;;
		*)
			echo "Invalid Option: $1"
			exit 1
			;;
	esac
done	

if [[ $norun != 1 ]]; then
	echo "-- running the blast application..."
	python3 $blast --port $port --query-count $qc --task-count $tc --name blast
fi

if [[ $txn == 1 ]]; then
	echo "-- plotting txn log..." 
	python3 $txn_plot $transactions_log $opt_png --fontsize 12
fi

if [[ $worker == 1 ]]; then
	echo "-- plotting worker performance..."
	python3 $wkpfm_plot $performance_log
fi

if [[ $xlsx == 1 ]]; then
	echo "-- converting performance file to xlsx..."
	python3 $convert $performance_log
fi

echo "All Done."