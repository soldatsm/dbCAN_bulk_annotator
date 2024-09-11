# dbCAN Annotator

## Information

This `python` script allows to annotate many genomes with the CAZy database at the same time. It uses the `multiprocess` package from python to run multiple `dbcan_run` scripts. 

The user can choose the number of processes so that the system is not overloaded. The list of genomes is split into `N` processes. Within the process, annotation is performed sequentially.

`IMPORTANT:` Script should be run in conda environment with dbCAN. This means that the original script `run_dbcan` should be available (in the `PATH`).

## Requirements

This script require orifinal [dbCAN](https://github.com/linnabrown/run_dbcan) on the computer 