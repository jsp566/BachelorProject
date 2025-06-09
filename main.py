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
    scripts = [
            #'graph_default_assymetric2-2_one_price.py',
            #'graph_default_assymetric3-1_one_price.py',
            #'graph_default_assymetric2-1-1_one_price.py',
            #'graph_default_2_firms_small_dif_qual.py',
            #'graph_default_2_firms_big_dif_qual.py',
            #'graph_default_assymetric2-1-1_one_price_true_nash.py',
            #'result_table.py',
            'graph_default_assymetric2-1_one_price_true_nash.py',            
            'graph_nash.py',
            'graph_deviating_agent.py',
            #'graph_default_mono.py',
            #'graph_default_mono_0_init_no_convergence.py',
            #'graph_default_mono_0_init_no_convergence_one_price.py',
            #'graph_default_mono_no_convergence.py',
            #'graph_default_mono_no_convergence_one_price.py',
            #'graph_default_mono_no_exploration.py',
            #'graph_default_2_firms.py',
            #'graph_default_assymetric2-1-1_one_price.py',
            #'graph_default_assymetric2-1.py',
            #'graph_default_assymetric2-1_one_price.py',
            
            #'graph_default_assymetric2-2.py',
            #'graph_default_assymetric2-2_half_price.py',
            #'graph_default_2_firms_dif_qual.py',
            #'graph_default_assymetric2-2_one_price_true_nash.py',
            #'graph_default_assymetric3-1_one_price_true_nash.py',
            
            #'graph_default_3_firms.py',
            #'graph_merger.py',
            #'graph_default_4_firms.py',
            #'graph_default_5_firms.py',
            #'graph_discount_factor.py',
            #'graph_discount_factor_multifirm.py',
            #'graph_discount_factor_multiproduct.py',
            #'graph_discount_factor_together.py',
            #'graph_mu.py',
            #'graph_firms_boxplot.py',
            #'graph_firms_more_boxplot.py',
            #'graph_heatmap_alpha_beta.py',
    ]
    execute_scripts(scripts)

if __name__ == "__main__":
    main()