import os

def setup_directories(figs_dir_path):
    if not os.path.exists(figs_dir_path):
        os.makedirs(figs_dir_path)
