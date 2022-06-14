import os
import re

class Shortcode:
    def __init__(self, path, shortcode_type, fullname, source_repo, total_count=0, pages=[], repos={}) -> None:
        self = self
        self.path = path
        self.type = shortcode_type
        self.fullname = fullname
        self.source_repo = source_repo
        self.total_count = total_count
        self.pages = pages
        self.repos = repos

    def __str__(self):
        return self.fullname

    def __repr__(self):
        return self.fullname

class Repo:
    def __init__(self, name, vendor_docs_path, vendor_content_path, vendor_shortcodes_path, repo_docs_path, repo_content_path, repo_shortcodes_path, additional_content_paths = None):
        self = self
        self.name = name
        self.vendor_docs_path = vendor_docs_path
        self.vendor_content_path = vendor_content_path
        self.vendor_shortcodes_path = vendor_shortcodes_path
        self.repo_docs_path = repo_docs_path
        self.repo_content_path = repo_content_path
        self.repo_shortcodes_path = repo_shortcodes_path
        self.additional_content_paths = additional_content_paths

    def __str__(self):
        return self.name

repos_dict = {
    'automate': 'automate',
    'chef_server': 'chef-server',
    'chef_workstation': 'chef-workstation',
    'chef_web_docs': 'chef-web-docs',
    'desktop_config': 'desktop-config',
    'effortless': 'effortless',
    'supermarket': 'supermarket',
    'habitat': 'habitat',
    'inspec': 'inspec',
    'inspec_alicloud': 'inspec-alicloud',
    'inspec_aws': 'inspec-aws',
    'inspec_azure': 'inspec-azure',
    'inspec_habitat': 'inspec-habitat',
}

exclude_shortcode_list = [
'danger.html',
'fontawesome.html',
'foundation_tab.html',
'foundation_tabs_panel.html',
'foundation_tabs_panels.html',
'foundation_tabs.html',
'note.html',
'readFile_shortcode.html',
'responsive-table.html',
'reusable_text_versioned.html',
'warning.html',
'relref.html',
'README.md'
]

excluded_files = ['.DS_Store', 'README.md']

def return_vendor_doc_paths(repo):
    """Returns the path to repo docs in chef-web-docs"""
    vendor_prefix = os.path.dirname('../../chef-web-docs/_vendor/github.com/')
    # print("Printing repo: " + str(repo))
    if repo == 'chef-web-docs':
        vendor_doc_path = None
        vendor_content_path = None
        vendor_shortcode_path = None
    elif 'inspec' in str(repo):
        vendor_doc_path = vendor_prefix + '/inspec/' + str(repo) + "/docs-chef-io/"
    elif 'habitat' in str(repo):
        vendor_doc_path = vendor_prefix + '/habitat-sh/habitat/components/docs-chef-io/'
        # print("" + vendor_doc_path)
    else:
        if str(repo) == 'automate':
            vendor_doc_path = vendor_prefix + '/chef/automate/components/docs-chef-io/'
        else:
            vendor_doc_path = vendor_prefix + '/chef/' + str(repo) + '/docs-chef-io/'

    try:
        vendor_content_path
    except NameError:
        vendor_content_path = vendor_doc_path + 'content/'
        vendor_shortcode_path = vendor_doc_path + 'layouts/shortcodes/'

    if vendor_doc_path != None:
        if not os.path.isdir(vendor_doc_path):
            vendor_doc_path = None
        if not os.path.isdir(vendor_content_path):
            vendor_content_path = None
        if not os.path.isdir(vendor_shortcode_path):
            vendor_shortcode_path = None

    return vendor_doc_path, vendor_content_path, vendor_shortcode_path

def return_repo_doc_paths(repo):
    """returns the shortcodes and content directories of each repo."""
    repo_path_prefix = os.path.dirname('../../')

    if 'automate' in str(repo) or 'habitat' in str(repo) and 'inspec-' not in str(repo):
        docs_path = repo_path_prefix + '/' + str(repo) + '/components/docs-chef-io/'
    elif repo == 'chef-web-docs':
        docs_path = repo_path_prefix + '/' + str(repo) + '/'
    else:
        docs_path = repo_path_prefix + '/' + str(repo) + '/docs-chef-io/'

    docs_shortcodes_path = docs_path + 'layouts/shortcodes/'
    docs_content_path = docs_path + 'content/'

    if repo == 'chef-web-docs':
        additional_content_paths = [
            '../../chef-web-docs/data/infra/resources/',
            '../../chef-web-docs/_vendor/github.com/chef/desktop-config/docs-chef-io/data/desktop/resources/',
            '../../chef-web-docs/themes/docs-new/layouts/_default/',
            '../../chef-web-docs/layouts/shortcodes/',
            ]
    else:
        additional_content_paths = None


    if not os.path.isdir(docs_shortcodes_path):
        docs_shortcodes_path = None

    return docs_path, docs_content_path, docs_shortcodes_path, additional_content_paths


def create_repo_class_object(self):
    """creates a Repo object from the name of repo using return_vendor_doc_paths and return_repo_doc_paths"""
    name = self
    self_vendor_docs_path, self_vendor_content_path, self_vendor_shortcodes_path  = return_vendor_doc_paths(name)
    self_repo_path, self_content_path, self_shortcodes_path, additional_content_paths = return_repo_doc_paths(name)
    class_object = Repo(
        name = name,
        vendor_docs_path = self_vendor_docs_path,
        vendor_content_path = self_vendor_content_path,
        vendor_shortcodes_path = self_vendor_shortcodes_path,
        repo_docs_path = self_repo_path,
        repo_content_path = self_content_path,
        repo_shortcodes_path = self_shortcodes_path,
        additional_content_paths = additional_content_paths
        )
    return class_object

def return_repo(file_path):
    """get the repo that a file is in from the file_path"""
    vendored_repo_file_path_regex = r'_vendor\/github\.com\/[\w|-]+\/([\w|-]+)\/'
    if 'chef-web-docs/content' in file_path or 'chef-web-docs/layouts/shortcodes' in file_path or 'chef-web-docs/data/infra/resources' in file_path or 'chef-web-docs/themes/docs-new/' in file_path:
        repo = 'chef-web-docs'
    else:
        # print(file_path)
        repo_match = re.search(vendored_repo_file_path_regex, file_path)
        repo = repo_match.group(1)
        if repo == None:
            raise Exception("Sorry, no matching repo.")
    try:
        repo
    except:
        raise Exception("Sorry, repo is undefined.")
    return repo


def get_org_from_doc_path(doc_path):
    """Returns the github organization from the repo/doc path"""
    if 'habitat' in doc_path:
        org = 'habitat-sh'
    elif 'inspec' in doc_path:
        org = 'inspec'
    else:
        org = 'chef'
    return org


for key, value in repos_dict.items():
    repo_object = create_repo_class_object(repos_dict[key])
    repos_dict[key] = repo_object
