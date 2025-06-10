import os

folder_path = '/path/to/folder'
for filename in os.listdir(folder_path):
    if filename.startswith('prefix_'):
        new_filename = filename.replace('prefix_', 'new_prefix_')
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
