# dbCAN Bulk Annotator

## Information

This `python` script allows to annotate many genomes with the CAZy database at the same time. It uses the `multiprocess` package from python to run multiple `dbcan_run` scripts in parallel. 

The list of genomes is split between `N` numbers of `run_dbcan` script (it can be set by option `-p/--pools`). Within them, annotation is performed sequentially. Basically if you have 50 genomes/proteomes, and you chose `-p` 10, than it will run `50/10 = 5` run_dbcan scripts in parallel. Each script will annotate 10 genomes/proteomes. And EACH of run_dbcan will consume number of cpus, set by `--cpus` option. So the user should choose the number of processes so that the system is not overloaded.

`IMPORTANT:` Script should be run in the conda environment with dbCAN. This means that the original script `run_dbcan` should be available (in the `PATH`).

`More IMPORTANT:` That script has no power over HMMER and other programs that execute run_dbcan. This means that you cannot abort them by aborting dbCAN Bulk Annotator. (Manually, this can be done via htop by sending a kill signal to HMMER and the other programs that were executed via run_dbcan). So, before executing the script, check everything.

## Requirements

1. The original [dbCAN](https://github.com/linnabrown/run_dbcan) on the computer 
2. Python version >=3.7