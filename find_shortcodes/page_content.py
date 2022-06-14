###
# Find references to shortcodes in Markdown pages, templates, and yaml files.
###

"""Module os for opening files. Module re for handling regular expressions."""
import os
import re
from . import config


html_shortcode_regex = r'{{< ([\w|\_|\-]+) ?[\w|\=|\"|\_|\/]* >}}'
html_shortcode_subdir_regex = r'{{< [\w|\-]+\/{1}([\w|\/]+) ?[\w|\=|\"|\_|\/]* >}}'
md_shortcode_regex = r'{{% ([\w|\-]+) ?[\w|\"|\=|\:]* %}}'
md_shortcode_subdir_regex = r'{{% [\w|\-]+\/{1}([\w|\/|\-]+) ?[\w|\"|\=|\:]* %}}'
readFile_shortcode_regex = r'{{ readFile \"layouts\/shortcodes\/(\w+\.md)\"'
other_readFile_shortcode_regex = r'{{< readFile_shortcode file=\"([\w]+\.md)\"'
other_readFile_shortcode_file_path_regex = r'{{< readFile_shortcode file_path=\"layouts\/shortcodes\/([\w]+\.md)\"'
reusable_text_versioned_regex = r'{{< reusable_text_versioned file=\"(\w+)\" >}}'
yaml_file_shortcode_regex = r'shortcode: (\w+\.md)'
template_shortcode_ref_regex = r"{{ \$shortcode := \"layouts\/shortcodes\/(\w+\.md)\""


list_of_regexes = [
    template_shortcode_ref_regex,
    readFile_shortcode_regex,
    other_readFile_shortcode_regex,
    other_readFile_shortcode_file_path_regex,
    yaml_file_shortcode_regex
]

list_of_md_regexes = [
    md_shortcode_regex,
    reusable_text_versioned_regex,
    md_shortcode_subdir_regex
]

list_of_html_regexes = [
    html_shortcode_regex,
    html_shortcode_subdir_regex
]


def walk_dir(content_dir):
    """returns list of file paths of markdown pages in a directory"""
    list_of_file_paths = []
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file not in config.excluded_files:
                # print(file)
                file_path = root + '/' + file
                # print(file_path)
                list_of_file_paths.append(file_path)
    return list_of_file_paths

def open_file(file_path):
    """Open a file path and return the page content"""
    with open(file_path, encoding="utf-8") as file_object:
        file_text = file_object.read()

    return file_text

def search_shortcodes(text):
    """Look through the text in a page for shortcodes"""
    shortcode_list = []
    for regex in list_of_html_regexes:
        for match in re.finditer(regex, text):
            shortcode = match.group(1)
            shortcode_list.append(shortcode + '.html')

    for regex in list_of_md_regexes:
        for match in re.finditer(regex, text):
            shortcode = match.group(1)
            shortcode_list.append(shortcode + '.md')

    for regex in list_of_regexes:
        for match in re.finditer(regex, text):
            shortcode = match.group(1)
            shortcode_list.append(shortcode)


    shortcode_list = [code for code in shortcode_list if not code.startswith('/')]
    shortcode_list = [code for code in shortcode_list if code not in config.exclude_shortcode_list]
    return shortcode_list

## Create list of content directory paths
# docs_content_paths = [path + '/content' for path in config.doc_paths]

## Add infra resource yaml files and desktop resource yaml files
# docs_content_paths.append('../../chef-web-docs/data/infra/resources')
# docs_content_paths.append('../../chef-web-docs/_vendor/github.com/chef/desktop-config/docs-chef-io/data/desktop/resources')
# docs_content_paths.append('../../chef-web-docs/themes/docs-new/layouts/_default')
# docs_content_paths.append('../../chef-web-docs/layouts/shortcodes')

docs_content_paths = []
for key, value in config.repos_dict.items():
    if config.repos_dict[key].vendor_content_path is not None:
        docs_content_paths.append(config.repos_dict[key].vendor_content_path)
    if config.repos_dict[key].additional_content_paths != None:
        docs_content_paths.extend(config.repos_dict[key].additional_content_paths)
    if key == 'chef_web_docs':
        docs_content_paths.append(config.repos_dict[key].repo_content_path)

# print(docs_content_paths)

list_of_content_file_paths = []
for path in docs_content_paths:
    paths = walk_dir(path)
    list_of_content_file_paths.extend(paths)


def return_pages_with_shortcodes(list_of_content_paths):
    return_list_pages_with_shortcodes = []
    for file_path in list_of_content_paths:
        try:
            file_text = open_file(file_path)
        except:
            print('\nBad file: ')
            print(file_path)
            break
        listOfShortcodes = search_shortcodes(file_text)
        if len(listOfShortcodes) > 0:
            repo = config.return_repo(file_path)
            return_list_pages_with_shortcodes.append({'page': file_path, 'shortcodes': listOfShortcodes, 'repo': repo})
    # print('\n\n\n')
    return return_list_pages_with_shortcodes

pages_with_shortcodes = return_pages_with_shortcodes(list_of_content_file_paths)
