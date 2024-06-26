# kill processes with given the name or port

USER_NAME=$(whoami)
script_filename=$(basename "$0")

while [[ "$#" -gt 0 ]]; do
	case $1 in
		-p)
			process_info="$(lsof -i:$2 | grep -v PID)"
			pids=$(echo "$process_info" | grep -vE "grep|$script_filename" | awk '{print $2}' | uniq)
			if [[ -n $pids ]]; then
				echo pids = ${pids[*]} are being killed ...
				kill -9 $pids
			else
                echo "no process found"
            fi
			shift 2
			;;
		-n)
			pids="$(ps aux | grep $USER_NAME  | grep "$2" | grep -vE "grep|$script_filename" | tr -s ' ' |  cut -d ' ' -f 2)"
            if [[ -n $pids ]]; then
				echo pids = ${pids[*]} are being killed ...
				kill -9 $pids
			else
                echo "no process found"
            fi
			shift 2
			;;
		-afs)
			pids="$(lsof | grep '__afs' | grep $USER_NAME | grep -vE "grep|$script_filename" | tr -s ' ' | cut -d ' ' -f 2)"
			if [[ -n $pids ]]; then
                echo pids = ${pids[*]} are being killed ...
                kill -9 $pids
            else
                echo "no process found"
            fi
			shift 1
			;;
		*)
			echo "Invalid Option: $1"
			exit 1
			;;
	esac
done
