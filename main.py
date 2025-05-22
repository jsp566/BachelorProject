#Init file for running the graphing functions
import subprocess
import os
import datetime

def execute_scripts(scripts):
    for script in scripts:
        try:
            print(f'{datetime.datetime.now()} Excecuting {script}')
            subprocess.run(["python", script], check=True)
            print(f'{datetime.datetime.now()} {script} executed successfully')
        except subprocess.CalledProcessError as e:
            print(f'{datetime.datetime.now()} Error executing {script}')
            print(e)
        except FileNotFoundError:
            print(f'{datetime.datetime.now()} {script} not found')
        except Exception as e:
            print(f'{datetime.datetime.now()} An unexpected error occurred while executing {script}')
            print(e)

def main():
    scripts = ['graph_default_assymetric2-2.py','graph_default_assymetric2-2_half_price.py','graph_default_assymetric2-2_one_price.py','graph_default_assymetric2-1_one_price.py','graph_default_assymetric2-1-1.py','graph_default_assymetric3-1.py','graph_default_assymetric2-1-1-1.py','graph_default_assymetric2-2-1.py','graph_default_assymetric3-1-1.py','graph_default_assymetric3-2.py','graph_default_assymetric4-1.py']
    #scripts = ['graph_default_4_firms.py','graph_default_5_firms.py']
    #scripts = ['graph_default_mono.py', 'graph_default.py','graph_default_3_firms.py','graph_default_assymetric.py', 'graph_merger.py', 'graph_default_2x2.py']
    execute_scripts(scripts)

if __name__ == "__main__":
    main()