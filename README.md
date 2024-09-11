# dbCAN annotator

## Information

This `python` script allow to make annotation of many genomes by dbCAN database at the same time. This uses `multiprocess` package from python to run several `dbcan_run`. 

User can choose number of processes so the system will not chock. List of genomes will be split to `n` processes. Within the process the annotation is executed sequentially.

`IMPORTANT:` Scriot shoud be run in conda environment with dbCAN. That means original script `run_dbcan` should be reachable (be in `PATH`)

## Requirements

This script require orifinal [dbCAN](https://github.com/linnabrown/run_dbcan) on the computer 