import pytest
from ..find_shortcodes.page_content import *
from ..find_shortcodes.config import *

file_paths = [
    {
        'path': '../../chef-web-docs/_vendor/github.com/inspec/inspec/docs-chef-io/content/inspec/resources/_index.md',
        'repo': 'inspec'
    },
    {
        'path': '../../chef-web-docs/_vendor/github.com/inspec/inspec-aws/docs-chef-io/content/inspec/resources/azure_streaming_analytics_function.md',
        'repo': 'inspec-aws'
    },
    {
        'path': '../../chef-web-docs/_vendor/github.com/habitat-sh/habitat/components/docs-chef-io/content/inspec/resources/azure_streaming_analytics_function.md',
        'repo': 'habitat'
    },
    {
        'path': '../../chef-web-docs/content/azure_streaming_analytics_function.md',
        'repo': 'chef-web-docs'
    },
    {
        'path': '../../chef-web-docs/_vendor/github.com/chef/automate/components/docs-chef-io/content/automate/azure_streaming_analytics_function.md',
        'repo': 'automate'
    },
]

def test_return_repo():
    for path in file_paths:
        assert return_repo(path.get('path')) == path.get('repo')

badPath = '../../chef-web-docs/_vendor/githubcom/chef/automate/components/docs-chef-io/content/automate/azure_streaming_analytics_function.md'

def test_raiseRepoPathException():
    with pytest.raises(Exception):
        return_repo(badPath)


def test_file_content_paths():
    """Test if docs content directory paths are properly added to list of docs content dir paths from class objects"""
    docs_content_paths = []
    for key, value in config.repos_dict.items():
        print(key)
        if config.repos_dict[key].vendor_content_path is not None:
            docs_content_paths.append(config.repos_dict[key].vendor_content_path)
        if config.repos_dict[key].additional_content_paths != None:
            docs_content_paths.extend(config.repos_dict[key].additional_content_paths)
            print(config.repos_dict[key].additional_content_paths)
        print(docs_content_paths)
        assert None not in docs_content_paths

    assert '../../chef-web-docs/data/infra/resources/' in docs_content_paths
    assert None not in docs_content_paths
