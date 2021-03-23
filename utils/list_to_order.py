from config import instance_es
from loader import bot

def list_to_order(frame, caption, type, path):

    if type==1:

        # open(instance_es.path_result, 'w').close()
        for row in frame:
            with open(path, 'a') as out:
                out.write('\n')

                out.write("======" + caption + "==============="+ '\n')
                out.write(row + '\n')
                out.close()



    else:

        # open(instance_es.path_result, 'w').close()

        for list in frame:

            with open(path, 'a') as out:
                out.write("=================SID====================")

            for row in list:
                with open(path, 'a') as out:
                    out.write('\n')
                    out.write(row + '\n')
                    out.write("=====================================")
                    out.close()








