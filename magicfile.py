import os
import shutil
import datetime

""" Creates a directory if it doesn't already exist """
def create_directory(parent_dir, directory):


    newpath = os.path.join(parent_dir, directory)

    # Checks if the folder already exists
    if not os.path.exists(newpath):
        os.mkdir(newpath)

    print(f"Directory {directory} created")
    return newpath

""" Lists files based on filetype limits and a default limit where filetype limits can specify
 the type & number of files that can be sorted and default being every filetype and file in a directory"""
def list_files(parent_dir, filetype_limits=None, default_limit=None):
    files = {}
    try:
        items = os.listdir(parent_dir)
        for item in items:
            item_path = os.path.join(parent_dir, item)
            if os.path.isfile(item_path):
                filetype = item[item.rindex(".") + 1:]
                if filetype not in files:
                    files[filetype] = []
                limit = filetype_limits.get(filetype, default_limit)
                if limit is None or len(files[filetype]) < limit:
                    files[filetype].append(item_path)
    except Exception as e:
        print(f"An error has occurred: {e}")
    return files

def get_file_type(parent_directory, files_dict):
    types = {}
    for filetype, file_list in files_dict.items():
        types[filetype] = file_list
        create_directory(parent_directory, filetype)
    return types


def sort_files(parent_directory, filetype_limits):
    
    # Loop only through the specified filetype
    for filetype, limit in filetype_limits.items():
        target_dir = os.path.join(parent_directory, filetype)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # Counter to store the number of files moved to ensure the limit
        count = 0
        for file in os.listdir(parent_directory):
            if file.endswith('.' + filetype):
                if limit is not None and count >= limit:
                    break  
                    
                file_path = os.path.join(parent_directory, file)
                new_file_path = os.path.join(target_dir, file)
                os.rename(file_path, new_file_path)
                count += 1
                print(f"Moved {file} to {target_dir}")



def rename_files(parent_directory, file_types, use_custom_name=False, custom_name="File"):
    for filetype, files in file_types.items():
        target_dir = parent_directory  

        # Dictionary to track counts of each new filename to avoid conflicts
        count = {}  

        for file in files:
            file_path = os.path.join(parent_directory, file) 
            if not os.path.isfile(file_path):
                continue  # Skip if it's not a file

            # Get creation time and prepare new file name (in the case that there's no custom name the ctime will be used instead)
            ctime = os.path.getctime(file_path)
            date_str = datetime.datetime.fromtimestamp(ctime).strftime("%Y%m%d")

            if use_custom_name:
                name_prefix = custom_name
            else:
                name_prefix = date_str

            # Generate the new file name
            base_new_name = f"{name_prefix}"
            new_file_name = f"{base_new_name}_{count.get(base_new_name, 0)}.{filetype}"
            new_file_path = os.path.join(target_dir, new_file_name)

            # Make sure we don't overwrite existing files
            while os.path.exists(new_file_path):
                count[base_new_name] = count.get(base_new_name, 0) + 1
                new_file_name = f"{base_new_name}_{count[base_new_name]}.{filetype}"
                new_file_path = os.path.join(target_dir, new_file_name)

            # Rename the file
            os.rename(file_path, new_file_path)
            print(f"Renamed {file_path} to {new_file_path}")

def change_file_type(parent_directory, old_filetype, new_filetype, limit=None):
    # Check and create a directory for old file types if it doesn't exist
    old_dir = os.path.join(parent_directory, old_filetype)
    if not os.path.exists(old_dir):
        print(f"No directory found for the specified filetype: {old_filetype}, attempting to create.")
        os.makedirs(old_dir, exist_ok=True)  # Safe guard to handle directory creation if it does not exist

    # Process files in the parent directory, not in the old_dir
    count = 0
    for file in os.listdir(parent_directory):
        if limit is not None and count >= limit:
            break
        if file.endswith('.' + old_filetype):
            old_file_path = os.path.join(parent_directory, file)
            new_file_name = file[:-len(old_filetype)] + new_filetype
            new_file_path = os.path.join(parent_directory, new_file_name)
            os.rename(old_file_path, new_file_path)
            print(f"Changed file type of {file} to {new_file_name}")
            count += 1
            
    if count == 0:
        print(f"No files with the .{old_filetype} extension found in {parent_directory}")

    # Rename the directory if all files were changed
    if limit is None or count == limit:
        new_dir = os.path.join(parent_directory, new_filetype)
        if not os.path.exists(new_dir):
            os.rename(old_dir, new_dir)
            print(f"Directory renamed from {old_dir} to {new_dir}")
        else:
            print(f"Directory for new filetype already exists: {new_dir}")




#path = r""
#iles_list = list_files(path)
#files_types = get_file_type(path, files_list)
#sort_files(path, files_types)
#rename_files(path, files_types, use_custom_name=True, custom_name="CoolFile")

#filetype_limits = {}
#default_limit = None
#custom_file_name = "Test"
#files_dict = list_files(path, filetype_limits, default_limit)
#files_types = get_file_type(path, files_dict)

#sort_files(path, files_types)
#rename_files(path, files_types, use_custom_name=True, custom_name=custom_file_name)




