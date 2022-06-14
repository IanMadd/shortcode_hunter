import pytest
from ..find_shortcodes.page_content import search_shortcodes

pageText = r'''

### Examples

The following examples show how the `data_bag_item` method can be used in a recipe.

#### Get a data bag, and then iterate through each data bag item

{{% infra_lang_data_bag %}}

#### Use the contents of a data bag in a recipe

The following example shows how to use the `data_bag` and `data_bag_item` methods in a recipe, also using a data bag named `sea-power`):


### Examples

The following example shows how the `data_bag` method can be used in a recipe.

#### Get a data bag, and then iterate through each data bag item

{{% infra_lang_data_bag %}}

## data_bag_item

{{% data_bag %}}

The `data_bag_item` method can be used in a recipe to get the contents of a data bag item.

{{% workstation/server_data %}}

'''

outputshortcode_list = ['infra_lang_data_bag.md', 'infra_lang_data_bag.md', 'data_bag.md', 'server_data.md']

def test_searchMultipleShortcodes():
    outputList = search_shortcodes(pageText)
    assert outputList == outputshortcode_list
