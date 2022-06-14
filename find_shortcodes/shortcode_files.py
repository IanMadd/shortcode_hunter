###
# Find shortcode files in layouts/shortcodes in all repositories with docs content
###
import os
from . import config


# def list_shortcode_dir_paths(path_list):
#     output_list = []
#     for path in path_list:
#         shortcode_file_path = path + "/" + config.shortcode_path
#         if os.path.isdir(shortcode_file_path):
#             output_list.append(shortcode_file_path)

#     return output_list


def list_shortcode_files(list_of_paths):
    """return a list of all shortcodes and a list of all duplicate shortcodes"""
    list_of_dup_files = []
    list_of_files = []
    for shortcode_path in list_of_paths:
        print(shortcode_path)
        for root, dirs, files in os.walk(shortcode_path):
            # print("Root: " + root)
            # for dir in dirs:
            #     print("Dir: " + dir)
            # list_dir_shortcode_files = os.listdir(shortcode_path)
            for file in files:
                # print('\nNew Shortcode: ')

                if file not in config.excluded_files:
                    file_path = os.path.join(root, file)
                    print(file_path)
                    # print(root, dirs, file)
                    # if len(dirs) > 0:
                    #     print(root + dirs[0] + "/" + file)

                    shortname = file.replace('.md', '', 1)
                    shortname = file.replace('.html', '', 1)

                    source_repo = config.return_repo(shortcode_path)


                    if ".md" in file:
                        shortcode_type = "MD"
                    elif ".html" in file:
                        shortcode_type = "HTML"

                    shortname = config.Shortcode(file_path, shortcode_type, file, source_repo)
                    print(shortname)
                    print(shortname.path)
                    print(shortname.type)
                    print(shortname.fullname)
                    print("\n\n\n")

                    if any(x.fullname == file for x in list_of_files):
                        list_of_dup_files.append(file_path)
                    else:
                        # print(shortname.fullname)
                        list_of_files.append(shortname)
    # print(list_of_dup_files)
    return list_of_files, list_of_dup_files


list_of_shortcode_dir_paths = []
for key, value in config.repos_dict.items():
    if config.repos_dict[key].vendor_shortcodes_path is not None:
        list_of_shortcode_dir_paths.append(config.repos_dict[key].vendor_shortcodes_path)
    if key == 'chef_web_docs':
        list_of_shortcode_dir_paths.append(config.repos_dict[key].repo_shortcodes_path)


list_of_shortcode_files, list_of_duplicate_shortcode_files = list_shortcode_files(list_of_shortcode_dir_paths)
