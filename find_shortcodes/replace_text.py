import re


def return_file_text(path):
    with open(path) as file_object:
        fileText = file_object.read()

    return fileText

def output_page(path, page_text):
    with open(path, 'w', encoding="UTF-8") as file_object:
        file_object.write(page_text)

def replace_shortcode_in_page(shortcode, page_path):
    shortcodeText = return_file_text(shortcode.path)
    pageText = return_file_text(page_path)
    regexString = shortcode.fullname.replace('.md', '', 1)
    shortcodeRegex = r'{{% ' + regexString + r' %}}'
    if (shortcodeMatch := re.search(shortcodeRegex, pageText, re.M)):
        shortcodeMatchStart = shortcodeMatch.start()
        shortcodeMatchEnd = shortcodeMatch.end()
        pageText = pageText[:shortcodeMatchStart] + shortcodeText + pageText[shortcodeMatchEnd:]
        output_page(page_path, pageText)

