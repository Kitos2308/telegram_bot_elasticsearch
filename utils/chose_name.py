def choose_name(list_name, list_prod: list, list_dev: list, exclude_list: list):
    for name in list_name:

        if name[-4:] == 'prod':
            list_prod.append(name)
        else:
            if name not in exclude_list:
                if name != 'vsphere':
                    list_dev.append(name)
    return set(list_prod), set(list_dev)


