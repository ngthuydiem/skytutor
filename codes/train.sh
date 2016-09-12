#!/bin/bash
        
# %E - Elapsed real time (in [hours:]minutes:seconds)
# %P - Percentage of the CPU that this job got, computed as (%U + %S) / %E i.e. CPU secs in user mode + CPU secs in system (kernel) mode / elapsed secs
# %M - Maximum resident set size of the process during its lifetime, in Kbytes
# python word2vec_optimized.py --train_data enwiki --eval_data questions-words.txt --save_path tf-models/

# /usr/bin/time -f "Runtime:\t%E minutes\nCPU percentage:\t%P\nMax memory:\t%M KB" python word2vec_tensorflow.py --train_data enwiki --eval_data questions-words.txt --save_path tf-models/

#/usr/bin/time -f "Runtime:\t%E minutes\nCPU percentage:\t%P\nMax memory:\t%M KB" python /home/ubuntu/tensorflow/tensorflow/models/embedding/word2vec_optimized.py --train_data /home/ubuntu/skytutor/word2vec/enwiki --eval_data /home/ubuntu/skytutor/word2vec/questions-words.txt --save_path /home/ubuntu/skytutor/word2vec/tf-models/

#/usr/bin/time -f "Runtime:\t%E minutes\nCPU percentage:\t%P\nMax memory:\t%M KB" python /home/ubuntu/skytutor/word2vec/word2vec_tensorflow.py --train_data /home/ubuntu/skytutor/word2vec/enwik10 --eval_data /home/ubuntu/skytutor/word2vec/questions-words.txt --save_path /home/ubuntu/skytutor/word2vec/tf-models/

LOG_FILE="log_train.txt"

declare -a algos=("skip-gram") #"cbow")
declare -a opts=("negative-sampling") #"hierarchical-softmax")
num_cores=4
#module=train_with_gensim.py
module=train_with_tensorflow.py

for algo in "${algos[@]}"
do
	for opt in "${opts[@]}"
	do
		input="enwik8-cleaned-10mb"
		echo "START: " "$input" "$algo" "$opt"
		CMD=`python $module --input_file ../data/$input --output_file ../models/$input-$algo-$opt --nthreads $num_cores --training_algorithm $algo --optimization_technique $opt`
		echo $CMD
		/usr/bin/time -f "Runtime:\t%E minutes\nCPU percentage:\t%P\nMax memory:\t%M KB" $CMD >>$LOG_FILE 2>&1
		echo "END: " "$input" "$algo" "$opt"
	done   
done
        
#CMD="python word2vec_gensim.py --input_file text8 --output_file text8_sg_ns --nthreads 16"
#CMD="python word2vec_tensorflow.py text1M questions-words.txt"

#/usr/bin/time -f "Runtime:\t%E minutes\nCPU percentage:\t%P\nMax memory:\t%M KB" $CMD

# python -c "import numpy as np; np.__config__.show()" # check blas and numpy settings
