valgrind --tool=memcheck --leak-check=full --show-leak-kinds=all --show-reachable=no python test.py > valgrind_output.txt 2>&1

python analyze_valgrind_log.py
