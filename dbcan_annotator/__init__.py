import os
import subprocess
from typing import Tuple
def annotator(*args) -> None:
    """
    Annotation of several proteomes by dbCAN database using multiprocessing.
    
    Parameters
    ----------
    *args : tuple
        A tuple of tuples containing:
        1. str: path to the folder with proteomes.faa to annotate
        2. str: path to dbCAN database files
        3. int: number of cpus for dbCAN sub programms (dbCAN_sub, HMMER)
        4. str: path to where dbCAN outputs will be placed
        5. tuple[int, int]: size of terminal window
    
    Returns
    -------
    None
    """
    for tup in args[0]: 

        genomes_lst = tup[0]
        db_path = tup[1]
        cpus = tup[2]
        output = tup[3]
        terminal_size = tup[4]
    
        fpath_folder_output = os.path.join(output, f"{genomes_lst.split('/')[-1]}_dbcan")

        os.mkdir(fpath_folder_output)
        subprocess.run(["run_dbcan", f"{genomes_lst}.faa", 
                        "protein",
                    "--db_dir", f"{db_path}",
                    "--dbcan_thread", f"{cpus}", 
                    "--tf_cpu", f"{cpus}", 
                    "--stp_cpu", f"{cpus}" ,
                    "--out_dir", f"{fpath_folder_output}"])
        
        print('\n')
        print('-' * terminal_size[0])
        print(f"{genomes_lst.split('/')[-1]} -- Done!")   
        print('-' * terminal_size[0])


def version_printer(terminal_size:Tuple[int, int]) -> None:
    """
    Prints version and author information of script.
    
    Parameters
    ----------
    terminal_size : Tuple[int, int]
        Size of terminal window.
    """
    script_name = 'dbCAN bulk annotator'
    base = 'Based on dbCAN <https://github.com/linnabrown/run_dbcan>'
    version = 'Version: 0.01'
    last_update = 'Updated: 09.09.24'
    author = 'Tulenkov A.S.'
    affiliation = 'Winogradsky Institute of Microbiology, RAS'

    name_margin = terminal_size[0]//2 - len(script_name)//2
    base_margin = terminal_size[0]//2 - len(base)//2
    version_margin = terminal_size[0]//2 - len(version)//2
    update_margin = terminal_size[0]//2 - len(last_update)//2
    author_margin = terminal_size[0]//2 - len(author)//2
    affiliation_margin = terminal_size[0]//2 - len(affiliation)//2

    #printing
    print('-' * terminal_size[0])
    print(f"{' ' * name_margin}{script_name}{' ' * name_margin}")
    print(f"{' ' * base_margin}{base}{' ' * base_margin}")
    print(f"{' ' * version_margin}{version}{' ' * version_margin}")
    print(f"{' ' * update_margin}{last_update}{' ' * update_margin}")
    print(f"{' ' * author_margin}{author}{' ' * author_margin}")
    print(f"{' ' * affiliation_margin}{affiliation}{' ' * affiliation_margin}")
    print('-' * terminal_size[0])