#Init file for running the graphing functions
import subprocess
import os

def execute_scripts(scripts):
    for script in scripts:
        try:
            print(f'Excecuting {script}')
            subprocess.run(["python", script], check=True)
            print(f'{script} executed successfully')
        except subprocess.CalledProcessError as e:
            print(f'Error executing {script}')
            print(e)
        except FileNotFoundError:
            print(f'{script} not found')
        except Exception as e:
            print(f'An unexpected error occurred while executing {script}')
            print(e)

def main():
    scripts = ['graph_default_4_firms.py','graph_default_5_firms.py']
    #scripts = ['graph_default_mono.py', 'graph_default.py','graph_default_3_firms.py','graph_default_assymetric.py', 'graph_merger.py', 'graph_default_2x2.py']
    execute_scripts(scripts)

if __name__ == "__main__":
    main()