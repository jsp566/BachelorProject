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

def main():
    scripts = ['graph_default.py','graph_heatmap_alpha_beta.py']
    execute_scripts(scripts)

if __name__ == "__main__":
    main()