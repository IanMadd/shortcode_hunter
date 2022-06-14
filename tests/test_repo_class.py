import pytest
import os
from ..find_shortcodes import config


def test_create_class_manually():
    vendor_docs_path = '../../chef-web-docs/_vendor/github.com/habitat-sh/habitat/components/docs-chef-io/'
    vendor_content_path = '../../chef-web-docs/_vendor/github.com/habitat-sh/habitat/components/docs-chef-io/content'
    vendor_shortcodes_path = '../../chef-web-docs/_vendor/github.com/habitat-sh/habitat/components/docs-chef-io/layouts/shortcodes/'
    repo_docs_path = '../../habitat/components/docs-chef-io/'
    repo_content_path = '../../habitat/components/docs-chef-io/content/'
    repo_shortcodes_path = '../../habitat/components/docs-chef-io/layouts/shortcodes/'
    repo = config.Repo('habitat', vendor_docs_path, vendor_content_path, vendor_shortcodes_path, repo_docs_path, repo_content_path, repo_shortcodes_path)
    assert repo.name == 'habitat'
    assert repo.vendor_docs_path == '../../chef-web-docs/_vendor/github.com/habitat-sh/habitat/components/docs-chef-io/'

def test_hab_repo_class_return_vendor_doc_path():
    repo = 'habitat'
    repo = config.create_repo_class_object(repo)
    assert repo.name == 'habitat'
    assert repo.vendor_docs_path == '../../chef-web-docs/_vendor/github.com/habitat-sh/habitat/components/docs-chef-io/'
    assert repo.vendor_content_path == '../../chef-web-docs/_vendor/github.com/habitat-sh/habitat/components/docs-chef-io/content/'
    assert repo.vendor_shortcodes_path is None
    assert repo.repo_docs_path == '../../habitat/components/docs-chef-io/'
    assert repo.repo_content_path == '../../habitat/components/docs-chef-io/content/'
    assert repo.repo_shortcodes_path is None

def test_inspec_repo_class_return_vendor_doc_path():
    repo = 'inspec-aws'
    repo = config.create_repo_class_object(repo)
    assert repo.vendor_docs_path == '../../chef-web-docs/_vendor/github.com/inspec/inspec-aws/docs-chef-io/'
    assert repo.vendor_content_path == '../../chef-web-docs/_vendor/github.com/inspec/inspec-aws/docs-chef-io/content/'
    assert repo.vendor_shortcodes_path == '../../chef-web-docs/_vendor/github.com/inspec/inspec-aws/docs-chef-io/layouts/shortcodes/'
    assert repo.repo_docs_path == '../../inspec-aws/docs-chef-io/'
    assert repo.repo_content_path == '../../inspec-aws/docs-chef-io/content/'
    assert repo.repo_shortcodes_path == '../../inspec-aws/docs-chef-io/layouts/shortcodes/'


def test_automate_repo_class_return_vendor_doc_path():
    repo = 'automate'
    repo = config.create_repo_class_object(repo)
    assert repo.vendor_docs_path == '../../chef-web-docs/_vendor/github.com/chef/automate/components/docs-chef-io/'
    assert repo.vendor_content_path == '../../chef-web-docs/_vendor/github.com/chef/automate/components/docs-chef-io/content/'
    assert repo.vendor_shortcodes_path == '../../chef-web-docs/_vendor/github.com/chef/automate/components/docs-chef-io/layouts/shortcodes/'
    assert repo.repo_docs_path == '../../automate/components/docs-chef-io/'
    assert repo.repo_content_path == '../../automate/components/docs-chef-io/content/'
    assert repo.repo_shortcodes_path == '../../automate/components/docs-chef-io/layouts/shortcodes/'

def test_chef_web_docs_repo_class_return_vendor_doc_path():
    repo = 'chef-web-docs'
    repo = config.create_repo_class_object(repo)
    assert repo.vendor_docs_path is None
    assert repo.vendor_content_path is None
    assert repo.vendor_shortcodes_path is None
    assert repo.repo_docs_path == '../../chef-web-docs/'
    assert repo.repo_content_path == '../../chef-web-docs/content/'
    assert repo.repo_shortcodes_path == '../../chef-web-docs/layouts/shortcodes/'

def test_listing_classes():
    """Test that paths listed in class objects actually exist"""

    assert config.repos_dict['automate'].vendor_docs_path == '../../chef-web-docs/_vendor/github.com/chef/automate/components/docs-chef-io/'
    assert config.repos_dict['chef_web_docs'].vendor_docs_path is None
    assert config.repos_dict['chef_web_docs'].vendor_shortcodes_path is None
    assert config.repos_dict['chef_server'].vendor_shortcodes_path == '../../chef-web-docs/_vendor/github.com/chef/chef-server/docs-chef-io/layouts/shortcodes/'
    for key, value in config.repos_dict.items():
        print(config.repos_dict[key].name)
        if key != 'chef_web_docs':
            if config.repos_dict[key].vendor_docs_path is not None:
                assert os.path.isdir(config.repos_dict[key].vendor_docs_path) is True
            if config.repos_dict[key].vendor_content_path is not None:
                assert os.path.isdir(config.repos_dict[key].vendor_content_path) is True
            if config.repos_dict[key].vendor_shortcodes_path is not None:
                assert os.path.isdir(config.repos_dict[key].vendor_shortcodes_path) is True
            assert config.repos_dict[key].additional_content_paths is None
        else:
            assert '../../chef-web-docs/data/infra/resources/' in config.repos_dict[key].additional_content_paths

        print(config.repos_dict[key].repo_docs_path)
        assert os.path.isdir(config.repos_dict[key].repo_docs_path) is True
        assert os.path.isdir(config.repos_dict[key].repo_content_path) is True
        if config.repos_dict[key].repo_shortcodes_path is not None:
            print(config.repos_dict[key].repo_shortcodes_path)

            assert os.path.isdir(config.repos_dict[key].repo_shortcodes_path) is True

            #../../inspec-azure/docs-chef-io/layouts/shortcodes/
