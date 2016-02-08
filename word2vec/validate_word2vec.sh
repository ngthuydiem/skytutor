#!/bin/bash
        
# %E - Elapsed real time (in [hours:]minutes:seconds)
# %P - Percentage of the CPU that this job got, computed as (%U + %S) / %E i.e. CPU secs in user mode + CPU secs in system (kernel) mode / elapsed secs
# %M - Maximum resident set size of the process during its lifetime, in Kbytes

LOG_FILE="log_word2vec_validate.txt"

declare -a algos=("skip-gram") # "cbow")
declare -a opts=("negative-sampling") # "hierarchical-softmax")

for algo in "${algos[@]}"
do
	for opt in "${opts[@]}"
	do
		input="enwiki"
		echo "$input" "$algo" "$opt"
		CMD="python word2vec_validate.py --model_file models/$input-$algo-$opt.model"
		/usr/bin/time -f "Runtime:\t%E minutes\nCPU percentage:\t%P\nMax memory:\t%M KB" $CMD >>$LOG_FILE 2>&1
	done   
done       