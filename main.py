"""Module json for outputting JSON files."""
import json
import shutil
import os
import re
from find_shortcodes import shortcode_files, page_content, replace_text, config


# Ranges through the list of shortcodes files and
# and then ranges through the list of pages with shortcodes
# finds all instances of a page with that shortcode
# then adds the list of pages to the shortcodes `pages` parameter.

for shortcode in shortcode_files.list_of_shortcode_files:
    pages = []
    repoDict = {}
    total_count = 0
    for page in page_content.pages_with_shortcodes:
        shortcode_list_in_page = page.get('shortcodes')
        if shortcode.fullname in shortcode_list_in_page:
            for shortcodeItem in shortcode_list_in_page:
                if shortcodeItem == shortcode.fullname:
                    total_count += 1
                    pages.append(page.get('page'))
                    repo = page.get('repo')

                    if repo not in repoDict:
                        repoDict[repo] = 1
                    else:
                        repoDict[repo] += 1

    setattr(shortcode, 'pages', pages)
    setattr(shortcode, 'repos', repoDict)
    setattr(shortcode, 'total_count', total_count)

# print(shortcode_files.list_of_shortcode_files)


outputDict = {}
for shortcode in shortcode_files.list_of_shortcode_files:
    if shortcode.total_count > 0:
        outputDict[shortcode.fullname] = {
            'source repo': shortcode.source_repo,
            'total_count': shortcode.total_count,
            'repos': shortcode.repos,
        }

with open("shortcodes.json", "w", encoding="utf-8") as outfile:
    json.dump(outputDict, outfile, sort_keys=True, indent=4)

# outputDict = {}
# for shortcode in shortcode_files.list_of_shortcode_files:
#     match = config.value_in_list(shortcode.repos, "chef-web-docs")
#     if shortcode.total_count > 0 and match == True and "inspec" not in shortcode.repos and shortcode.source_repo == "chef-web-docs":
#         outputDict[shortcode.fullname] = {
#             'source repo': shortcode.source_repo,
#             'total_count': shortcode.total_count,
#             'repos': shortcode.repos,
#         }

# with open("shortcodes.json", "w", encoding="utf-8") as outfile:
#     json.dump(outputDict, outfile, sort_keys=True, indent=4)

outputDict = {}
for shortcode in shortcode_files.list_of_shortcode_files:
    match = config.value_in_list(shortcode.repos, "chef-web-docs")
    if shortcode.total_count == 1 and match == True:
        outputDict[shortcode.fullname] = {
            'source repo': shortcode.source_repo,
            'total_count': shortcode.total_count,
            'repos': shortcode.repos,
        }

with open("shortcodes_one.json", "w", encoding="utf-8") as outfile:
    json.dump(outputDict, outfile, sort_keys=True, indent=4)

# outputDict = {}
# count = 0
# for shortcode in shortcode_files.list_of_shortcode_files:
#     if (shortcode.source_repo == 'chef-web-docs' and
#         len(shortcode.repos) > 1 and
#         shortcode.total_count > 0):
#             count += 1
#             outputDict[shortcode.fullname] = {
#                 'source repo': shortcode.source_repo,
#                 'total_count': shortcode.total_count,
#                 'repos': shortcode.repos,
#                 'path': shortcode.path,
#                 'review': False
#             }

# with open("workstation-shortcodes.json", "w", encoding="utf-8") as outfile:
#     json.dump(outputDict, outfile, sort_keys=True, indent=4)


# outputDict = {}
# count = 0
# for shortcode in shortcode_files.list_of_shortcode_files:
#     if (shortcode.source_repo == 'chef-web-docs' and
#         'chef-workstation' in shortcode.repos and
#         shortcode.total_count == 1 ):
#             count += 1
#             outputDict[shortcode.fullname] = {
#                 'source repo': shortcode.source_repo,
#                 'total_count': shortcode.total_count,
#                 'repos': shortcode.repos,
#                 'path': shortcode.path,
#                 'review': False,
#                 'pages': shortcode.pages
#             }

# with open("shortcodes-workstation-one.json", "w", encoding="utf-8") as outfile:
#     json.dump(outputDict, outfile, sort_keys=True, indent=4)

# for shortcode, value in outputDict.copy().items():
#     print('\n\n\n')
#     moving = True
#     review = True
#     print(shortcode)
#     print(value['repos'])
#     print(len(value['repos']))
#     if value['total_count'] == 1:
#         review = False
#         moving = False
#         shortcode_text = replace_text.return_file_text(value['path']).strip()
#         server_content_dir = config.repos_dict['chef_server'].repo_content_path
#         server_pages_list = page_content.walk_dir(server_content_dir)
#         replace_shortcode_regex = r'{{% ' + shortcode.replace('.md', '') + r' %}}'
#         for page in server_pages_list:
#             page_text = page_content.open_file(page)
#             page_text = re.sub(replace_shortcode_regex, shortcode_text, page_text, 0, re.M)
#             replace_text.output_page(page, page_text)

#         append_text = r'{{/* shortcode delete. Text moved to chef-server repo */}}'
#         shortcode_file_path = value['path']
#         file_text = page_content.open_file(shortcode_file_path)

#         file_text = file_text + '\n\n' + append_text + '\n'
#         replace_text.output_page(shortcode_file_path, file_text)

#     elif len(value['repos'].keys()) > 1:
#         chef_server_count = value['repos']['chef-server']
#         print(chef_server_count)
#         for k, v in value['repos'].items():
#             print('repo: {}, count: {}'.format(k, v))
#             if k != 'chef-server':
#                 if v >= chef_server_count:
#                     moving = False
#             if v > chef_server_count or v < chef_server_count:
#                 review = False
#     else:
#         review = False
#     if moving is True:
#         print('Move {}'.format(shortcode))
#         outputDict[shortcode]['moving'] = True
#     else:
#         print('Don\'t move {}'.format(shortcode))
#         outputDict[shortcode]['moving'] = False
#     if review:
#         print('Review this shorcode')
#         outputDict[shortcode]['review'] = True
#     print('\n\n\n')

# append_text = r'{{/* moved to chef-server repo */}}'
# server_repo_path = os.path.dirname('../../chef-server/docs-chef-io/')


# print(value['path'])

# for shortcode, value in outputDict.items():
#     if value['moving']:
#         """Copy item to chef-server repo and update references in chef-server docs"""
#         destPath = server_repo_path + '/layouts/shortcodes/chef-server/' + shortcode
#         print('Moving from: ' + str(value['path']))
#         print('Moving to: ' + destPath)
#         shutil.copy(value['path'], destPath)
#         shortcode_short_name = shortcode.replace('.md', '')
#         shortcode_regex = r'{{% ' + shortcode_short_name + r' %}}'
#         shortcode_replace = r'{{% chef-server/' + shortcode_short_name + r' %}}'
#         server_content_path = server_repo_path + '/content'
#         server_pages_list = page_content.walk_dir(server_content_path)
#         print(shortcode_regex)
#         print(shortcode_replace)
#         for page_file_path in server_pages_list:
#             page_text = page_content.open_file(page_file_path)
#             page_text = re.sub(shortcode_regex, shortcode_replace, page_text, re.M)
#             replace_text.output_page(page_file_path, page_text)

#         shortcode_file_path = value['path']
#         file_text = page_content.open_file(shortcode_file_path)

#         file_text = file_text + '\n\n' + append_text + '\n'
#         replace_text.output_page(shortcode_file_path, file_text)



# with open("chefServerShortcodes.json", "w", encoding="UTF-8") as outfile:
#     json.dump(outputDict, outfile, sort_keys=True, indent=4)


# review_dict = {}
# for shortcode, value in outputDict.items():
#     if value['total_count'] == 1 or value['review'] is True:
#         review_dict[shortcode] = {
#             'path': value['path'],
#             'total_count': value['total_count'],
#             'review': value['review'],
#             'repos': value['repos']
#         }


# with open("chefServerReview.json", "w", encoding="UTF-8") as outfile:
#     json.dump(review_dict, outfile, sort_keys=True, indent=4)

# outputDict = {}
# for shortcode in shortcode_files.list_of_shortcode_files:
#     if shortcode.total_count == 0:
#         outputDict[shortcode.fullname] = {'source repo': shortcode.source_repo, 'total_count': shortcode.total_count, 'repos': shortcode.repos}

# with open("shortcodesZero.json", "w") as outfile:
#     json.dump(outputDict, outfile, sort_keys=True, indent=4)
