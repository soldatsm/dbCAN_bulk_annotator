import argparse
import os
from datetime import datetime
from multiprocessing import Pool
import shutil
from . import annotator, version_printer

def argument_parser() -> argparse.ArgumentParser:
    """
    Argument parser for dbCAN bulk annotator.
    
    Returns
    -------
    argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input',
                        help='Path to the folder with proteomes.faa',
                        required=True,
                        type=str)
    parser.add_argument('-p','--pools',
                        help='Lenght of average sublist. Number of pools = number of sublists',
                        default=1,
                        type=int)
    parser.add_argument('-o','--output',
                        help='Path to where dbCAN outputs will be placed',
                        required=True,
                        type=str)
    parser.add_argument('-db', '--dbCAN_database',
                        help='Path to dbCAN database files',
                        required=True,
                        type=str)
    parser.add_argument('--cpus',
                        help='Choose numper of cpus for dbCAN sub programms (dbCAN_sub, HMMER). \
                            Default is half of available cpus',
                        default=os.cpu_count()//2,
                        type=int)
    return parser


def main():
    """
    Main function for dbCAN bulk annotator.
    
    This function parses arguments, prints version and author information,
    makes a list of all genomes in input folder, splits it into nested list
    for multiprocessing, run annotator on each pool of genomes, and prints
    final statistics.
    """
    parser = argument_parser()
    args = parser.parse_args()

    version_printer(terminal_size=shutil.get_terminal_size())
    
    terminal_size = shutil.get_terminal_size()
    script_start_time = datetime.now()

    abs_path_output = os.path.abspath(args.output)
    abs_path_input = os.path.abspath(args.input)

    dir_list = os.listdir(abs_path_input)

    dir_list = [(f"{abs_path_input}/{i.replace('.faa', '')}",
                 args.dbCAN_database, args.cpus,
                 abs_path_output, terminal_size)
                for i in dir_list]
    #creation of nested list for pools
    nested_list = [dir_list[i:i+args.pools]
                   for i in range(0, len(dir_list), args.pools)] 

    with Pool(processes=len(nested_list)) as p:
        #mapping function on genomes in each pool
        p.map(annotator , nested_list) 

    print('-' * terminal_size[0])
    print(f'Programm working time: {datetime.now() - script_start_time}')
    print(f'Number of annotated proteomes: {len(dir_list)}')
    print(f'Number of used processes: {len(nested_list)}')
    print('-' * terminal_size[0])
