import argparse
import os
from datetime import datetime
from multiprocessing import Pool
import shutil
import sys
from . import annotator, version_printer, folder_checker

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
                        help='Lenght of average sublist. It indicate amount of genomes that will be annotated in one process. More number, faster work, and higher demand on the CPU \
                        EXAMPLE: you have 50 genomes/proteomes, if you chose -p 10, than it will run 50/10 = 5 run_dbcan scripts in PARALLEL. Each script will annotate 10 genomes/proteomes. IMPORTANT: EACH of run_dbcan will consume number of cpus, set by --cpus option.',
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
                        help='Choose numper of cpus/threads for dbCAN sub programms (e.g.dbCAN_sub, HMMER). \
                        Default is 1.',
                        default=1,
                        type=int)
    parser.add_argument('--type', help='Chose input data type [protein, prok, meta].\
                        Make sure you chose the right option for your sequences.\
                        proteins -- in silico translated proteome,\
                        prok -- nucleotide assembly. Which will be annotated by Prokka,\
                        meta -- metagenome assemblied genome. Will be annotated with Prokka.', 
                        choices=['protein', 'prok', 'meta'], default='protein')
    return parser


def main() -> None:
    """
    Main function for dbCAN bulk annotator.
    
    This function parses arguments, prints version and author information,
    makes a list of all genomes in input folder, splits it into nested list
    for multiprocessing, run annotator on each pool of genomes, and prints
    final statistics.
    """
    parser = argument_parser()
    args = parser.parse_args()

    #print version of the script
    version_printer(terminal_size=shutil.get_terminal_size())
    
    terminal_size = shutil.get_terminal_size()
    script_start_time = datetime.now()

    abs_path_output = os.path.abspath(args.output)
    abs_path_input = os.path.abspath(args.input)
    dir_list = os.listdir(abs_path_input)

    #check if output folder is empty
    if not folder_checker(abs_path_output):
        print('There is some files in chose folder.')
        print('Please remove them and run script again')
        print('Exiting...')
        print('-' * terminal_size[0])
        sys.exit()

    #stats
    SEQ_NUMBER = len(dir_list)
    PARALLEL = int(SEQ_NUMBER/args.pools)

    dir_list = [(f"{abs_path_input}/{i}",
                 args.dbCAN_database, args.cpus,
                 abs_path_output, terminal_size, args.type)
                for i in dir_list]
    
    #creation of nested list for pools
    nested_list = [dir_list[i:i+args.pools]
                   for i in range(0, len(dir_list), args.pools)] 

    #Some messages 
    print(f'You chose {args.pools} number of pools.')
    print(f'It means each parallel process will has {args.pools} genomes/proteomes.')
    print(f'There will be {PARALLEL} run_dbcan scripts running in parallel.')
    print(f'And each of the parallel process will consume {args.cpus} threads.')
    print(f'In total {PARALLEL*args.cpus} threads.')
    print('Is it appropriate for your system?')
    proceed_answer = input('Continue ? Y/N: ')
    print('-' * terminal_size[0])
    if proceed_answer.lower() != 'y':
        sys.exit()

    with Pool(processes=len(nested_list)) as p:
        #mapping function on genomes in each pool
        p.map(annotator , nested_list) 

    print('-' * terminal_size[0])
    print(f'Programm working time: {datetime.now() - script_start_time}')
    print(f'Number of annotated proteomes: {len(dir_list)}')
    print(f'Number of used processes: {len(nested_list)}')
    print('-' * terminal_size[0])
