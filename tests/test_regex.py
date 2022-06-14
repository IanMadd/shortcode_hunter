from ..find_shortcodes.page_content import search_shortcodes

text1 = '''
### Resources

Chef InSpec has {{% inspec_count_resources %}} [resources](/inspec/resources/) ready to use--from Apache2 to ZFS pool.
If you need a solution that we haven’t provided, you can write your own [custom
resource](/inspec/dsl_resource/).

'''

def test_regex1():
    """Text if search_shortcodes returns the correct list of shortcodes in text1"""
    shortcode_list = search_shortcodes(text1)
    assert shortcode_list == ['inspec_count_resources.md']

text2 = '''

{{< azurerm_deprecated resource="azure_aks_cluster" >}}

Use the `azurerm_aks_cluster` InSpec audit resource to test properties of an Azure AKS Cluster.
'''

def test_regex2():
    """Text if search_shortcodes returns the correct list of shortcodes in text2"""
    shortcode_list = search_shortcodes(text2)
    assert shortcode_list == ['azurerm_deprecated.html']

