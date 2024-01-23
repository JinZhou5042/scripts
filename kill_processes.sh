# parse arguments by multiple characters

while [[ "$#" -gt 0 ]]; do
	case $1 in
		-p)
			# lsof -i:$2 | awk '{print $2}' | grep -v PID | xargs kill $3
			lsof -i:$2 | grep -v PID | tr -s ' ' | cut -d ' ' -f 2 | xargs kill -9
			shift 2
			;;
		-n)
			ps aux | grep jzhou24 | grep $2 | tr -s ' ' |  cut -d ' ' -f 2 | xargs kill -9 
			shift 2
			;;
		*)
			echo "Invalid Option: $1"
			exit 1
			;;
	esac
done
