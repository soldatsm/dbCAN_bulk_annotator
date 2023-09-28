import argparse
import os
import subprocess
from multiprocessing import Pool
from datetime import datetime

parser = argparse.ArgumentParser()

parser.add_argument('-input', help='Path to the folder with proteomes.faa', required=True, type=str)
parser.add_argument('-pools', help='Number of annotation to start at same time', default=4, type=int)
parser.add_argument('-output', help='Path to where dbCAN outputs will be placed', required=True, type=str)
parser.add_argument('-dbCAN_database', help='Path to dbCAN database files', default='/hdd/dbCAN_db/db', required=True, type=str)
parser.add_argument('-cpus', help='Choose numper of cpus for dbCAN sub programms (dbCAN_sub, HMMER)', default=8, type=int)

args = parser.parse_args()

def annotator(lst):

    for genome in lst:

        fpath_folder_output = os.path.join(args.output, genome.split('/')[-1])

        os.mkdir(fpath_folder_output)

        subprocess.run(["run_dbcan", f"{genome}.faa", 
                        "protein",
                       "--db_dir", f"{args.dbCAN_database}",
                       "--dbcan_thread", f"{args.cpus}", 
                       "--tf_cpu", f"{args.cpus}", 
                       "--stp_cpu", f"{args.cpus}" ,
                       "--out_dir", f"{fpath_folder_output}"])

        print('-------------------------------------------------------------')
        print(f"{genome.split('/')[-1]} -- Done!")   
        print('-------------------------------------------------------------') 

if __name__ == '__main__':

    script_start_time = datetime.now()

    args.output = os.path.abspath(args.output)
    args.input = os.path.abspath(args.input)

    dir_list = os.listdir(args.input)

    dir_list = [f"{args.input}/{i.replace('.faa', '')}" for i in dir_list]
    nested_list = [dir_list[i:i+args.pools] for i in range(0, len(dir_list), args.pools)] #creation of nested list for pools


    p = Pool(processes=args.pools)
    p.map(annotator, nested_list) #mapping function on genomes in each pool

    print('-------------------------------------------------------------')
    print(f'Programm Working Time: {script_start_time - datetime.now()}')

