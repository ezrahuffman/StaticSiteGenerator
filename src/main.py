from textnode import *
import os
import shutil

def main():
    static_dir = "static"
    public_dir = "public"
    remove_dir(public_dir)
    copy_from_directory(static_dir, public_dir)

def copy_from_directory(from_dir, to_dir):
    if not os.path.exists(from_dir):
        raise Exception("From directory is not valid")
    if not os.path.exists(to_dir):
        os.mkdir(to_dir)
    
    from_dir_contents = os.listdir(from_dir)
    for content in from_dir_contents:
        full_to_path =  os.path.join(to_dir, content)
        full_from_path = os.path.join(from_dir, content)
        if os.path.isfile(full_from_path):
            shutil.copy(full_from_path, full_to_path)
            print(f"copy file from {full_from_path} to {full_to_path}")
        else:
            os.mkdir(full_to_path)
            copy_from_directory(full_from_path, full_to_path)

def remove_dir(dir):
    if not os.path.exists(dir):
        print(f"directory {dir} doesn't exist, do nothing")
        return
    print(f"remove entire directory: {dir}")
    shutil.rmtree(dir)
            


if __name__ == "__main__":
    main()