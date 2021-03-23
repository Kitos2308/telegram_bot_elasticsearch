import os
from analytic.es import show_route,get_id_route,add_prohibited_route,get_route,convert_time,get_ip,get_sid, \
    get_last_time, get_certain_data, get_index_time, delete_route_


class Analytic_es():

    def __init__(self):

        self.file_name_routes = 'routes.txt'
        self.result = 'result.txt'
        self.result_vsphere = 'result_vsphere.txt'
        self.result_bsapi= 'bs_api.txt'
        self.result_wallet='wallet.txt'
        self.path_wallet = os.path.abspath(self.result_wallet)
        self.path_vsphere = os.path.abspath(self.result_vsphere)
        self.path_result = os.path.abspath(self.result)
        self.path_routes = os.path.abspath(self.file_name_routes)
        self.path_bsapi= os.path.abspath(self.result_bsapi)
        self.choice = "None"
        self.bug = "None"
        self.time_critical = 0
        self.time_error = 0
        self.time_ = 0
        self.time_sequence = 0
        self.confirmroute = "api/v1/confirm"
        self.registerroute = "api/v1/register"
        self.loginroute = "api/v1/login"
        self.microservice= {}





    def get_last_time(self, index):
        get_last_time(index)


    def find_ip(self, index,es):

        index,frame_data=get_index_time(index, es)

        #first of all we need find unique sid
        unique_sid=get_sid(frame_data)

        for sid in unique_sid:
            if sid=="None":
                pass
            else:
                host, analyze_inside_sid=get_certain_data(index, sid, es )

                ip = get_ip(analyze_inside_sid)



                try:
                    time_frame = convert_time(analyze_inside_sid)
                except NameError:
                    print("frame is not define, because level of log doesn't exist")
                    pass

                length = len(analyze_inside_sid)
                cnt = 0
                result_list = []
                while length - 1 > cnt:
                    try:
                        if ip[cnt] == ip[cnt + 1]:

                            pass
                        else:
                            try:
                                delta = time_frame[cnt + 1] - time_frame[cnt]
                            except IndexError:
                                pass
                            # print(time_frame[cnt])
                            # print(time_frame[cnt + 1])
                            # print(delta.seconds)
                            if (delta.seconds < 2):
                                result_list.append(analyze_inside_sid[cnt])
                                result_list.append(analyze_inside_sid[cnt + 1])
                    except ImportError:
                        pass

                    cnt = cnt + 1

                return result_list

    def prohibited_combination(self, index, es):
        frame_index = get_index_time(index, es)
        unique_sid = get_sid(frame_index[1])
        result = []

        for sid in unique_sid:
            if sid=="None":
                sid=" "

            host,certain_sid=get_certain_data(index, sid, es)
            list_result=[]
            cnt=0
            length =len(certain_sid)


            while length-1>cnt:
                tmp=certain_sid[cnt]
                tmp_route=get_route(tmp)
                # print("\n")
                # print(tmp_route)
                tmp_next_route=get_route(certain_sid[cnt+1])
                # print(tmp_next_route)
                # print(tmp)
                if tmp_route.find("login") != -1:
                    if tmp_next_route.find("register") !=-1 or tmp_next_route.find("confirm") != -1:
                        list_result.append(tmp)
                        list_result.append(certain_sid[cnt+1])
                        # print("========================================")

                if tmp_route.find("confirm") != -1:
                    if tmp_next_route.find("register") != -1:
                        list_result.append(tmp)
                        list_result.append(certain_sid[cnt+1])
                cnt=cnt+1
            if list_result:
                result.append(list_result)


        return result


    def add_prohibited_route(self,route, username_es, pass_es):

        add_prohibited_route(route, username_es, pass_es)

    def delete_prohibited_route(self,route, username_es, pass_es):

        id=get_id_route(route, username_es, pass_es)

        for delete_route in id:
            delete_route_(delete_route, username_es, pass_es)
        if id:
            return True
        else:
            return False



    def show_prohibited_route(self, username_es, pass_es):
        routes=show_route("prohibited_routes", username_es, pass_es)

        return routes



    def prohibited_routes(self, index, es, username_es, pass_es):
        list_routes = self.show_prohibited_route(username_es, pass_es)

        list_answer=[]
        for row in list_routes:
            index,result = get_certain_data(index, row, es)
            if result:
                for row_ in result:
                    list_answer.append(row_)

        return list_answer




