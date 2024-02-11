import os

def get_mount_point(path):
    while not os.path.ismount(path):
        path = os.path.dirname(path)
    return path

# Example usage
path_to_file = "/home/oracle/scripts/practicedir_abi_sep23"
mount_point = get_mount_point(path_to_file)
print("The actual path to the disk is: {}".format(mount_point))
