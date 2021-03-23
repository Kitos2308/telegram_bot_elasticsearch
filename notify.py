from utils.list_to_order import list_to_order
def notify(list_error, list_critical, list_prohibited, list_prohibited_db,list_ip,path):
    flag=0
    if list_error:
        flag=1
        list_to_order(list_error, "ERROR",1,path)

    if list_critical:
        flag=1
        list_to_order(list_critical, "CRITICAL", 1, path)


    if list_prohibited:
        flag=1
        list_to_order(list_prohibited, "Запрещенные переходы login,confirm", 2, path)

    if list_prohibited_db:
        flag=1
        list_to_order(list_prohibited_db, "Запрещенные переходы из базы", 1, path)

    if list_ip:
        flag=1
        list_to_order(list_ip, "Запрещенные АПИ", 1, path)

    if flag==1:
        return True
    else:
        return False