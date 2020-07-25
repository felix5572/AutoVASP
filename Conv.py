#!/usr/bin/env python3

# for ii in `ls -d -1 ./new_job/*-*`;do cd $ii && ln -s ../../sub.sh ./ && sbatch sub.sh && cd ../../;done
#%%
import os, sys, json, argparse, glob, shutil
import re
import numpy as np

def conv_make_tasks(jdata, output_dir='new_job'):
    POSCAR=jdata.get('POSCAR')
    INCAR=jdata.get('INCAR')
    POTCAR=jdata.get('POTCAR')
    test=jdata.get('test')

    test_KSPACING=test.get('KSPACING', [])
    test_ENCUT=test.get('ENCUT', [])
    test_SIGMA=test.get('SIGMA', [])

    KSPACING_sub_p=re.compile(r'KSPACING\s*=.*')
    ENCUT_sub_p=re.compile(r'KSPACING\s*=.*')
    SIGMA_sub_p=re.compile(r'SIGMA\s*=.*')

    with open(INCAR, 'r') as f:
        INCAR_content = f.read()
    
    os.mkdir(f'./{output_dir}')
    p_map={'KSPACING':(test_KSPACING,KSPACING_sub_p,),
            'ENCUT': (test_ENCUT,ENCUT_sub_p,),
            'SIGMA': (test_SIGMA,SIGMA_sub_p,)}
    for k,(test_list,p) in p_map.items():
        for ii in test_list:
            dir_name=f'{output_dir}/{k}-{ii}'
            os.mkdir(f'./{dir_name}')
            os.symlink(f'../../{POTCAR}', f'./{dir_name}/POTCAR')
            os.symlink(f'../../{POSCAR}', f'./{dir_name}/POSCAR')
            with open(f'./{dir_name}/INCAR', 'w') as f:
                f.write(p.sub(f'{k} = {ii}', INCAR_content))


def _main():
    parser = argparse.ArgumentParser(description="Compute free energy by Hamiltonian TI")
    subparsers = parser.add_subparsers(title='Valid subcommands', dest='command')

    parser_gen = subparsers.add_parser('gen', help='Generate a job')
    parser_gen.add_argument('PARAM', type=str ,
                            help='json parameter file')
    parser_gen.add_argument('-o','--output', type=str, default = 'new_job',
                            help='the output folder for the job')

    args = parser.parse_args()

    if args.command == 'gen' :
        jdata = json.load(open(args.PARAM, 'r'))
        conv_make_tasks(jdata=jdata, output_dir=args.output)

if __name__ == '__main__' :
    _main()



# %%
