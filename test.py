my_list = ["apples", "pears"] # return true

my_other_list = ["apples"] #return false

def value_in_list(check_list, check):
    """Return True if any value in list does not match string"""
    val = False
    for item in check_list:
        if item != check:
            val = True
    return val

print(value_in_list(my_list, "apples"))


print(value_in_list(my_other_list, "apples"))
