import time
import os
import pandas as pd
import datetime as dt
import numpy as np





class Analytic():

    def __init__(self):

        self.file_name_routes = 'routes.txt'
        self.result = 'result.txt'
        self.path_result = os.path.abspath(self.result)
        self.path_routes = os.path.abspath(self.file_name_routes)
        self.choice="None"
        self.bug="None"
        self.time_critical=0
        self.time_error=0
        self.time_=0
        self.time_sequence=0
        self.confirmroute="api/v1/confirm"
        self.registerroute="api/v1/register"
        self.loginroute="api/v1/login"

    def return_result(self):
        return self.path_result




    def find_secuence(self, frame, time):
        mask_sid = frame["sid"]  # mask for sid

        mask_drop_sid = mask_sid.drop_duplicates(keep='first', inplace=False)

        result_list=[]
        mask_time=frame['date']
        frame_time=frame.loc[mask_time>time]
        if not frame_time.empty:
            for mask in mask_drop_sid:
                frame_sid=frame_time.loc[mask_sid==mask]
                er1=self.sequence(frame_sid, 'confirm', 'register')
                er2=self.sequence(frame_sid, 'login', 'confirm')
                er3=self.sequence(frame_sid, 'login', 'register')
                if er1:
                    result_list.append(er1)
                if er2:
                    result_list.append(er2)
                if er3:
                    result_list.append(er3)

            if not result_list:
                return False
            else:
                return result_list






    def sequence(self, frame, route1, route2):
        length=len(frame.index)
        cnt=-1
        api_routes=frame['api_route']
        list=[]

        for items in api_routes:
            cnt=cnt+1
            if items != None:
                state=items.find(route1)
                if state !=-1:
                    if cnt != length-1:
                        route=frame.iat[cnt+1,5]
                        state2=route.find(route2)
                        if state2 != -1:
                            list.append(frame.iloc[cnt,:])
                            list.append(frame.iloc[cnt+1,:])

        return list



    def timedelta(self, time1,time2, frame1, frame2):
        delta=time2-time1

        if (delta.seconds< 2) :

            with open(self.result, 'a') as out:
                out.write("===========================================" + '\n')
                out.write(str(frame1) + '\n')
                out.write(str(frame2) + '\n')
                out.write("===========================================" + '\n')


                


    def prohibit_route(self, frame, time):


        result = self.read_routes()

        cnt_rows=len(result.index)
        mask_result=frame['api_route']

        list=[]
        cnt=0
        while cnt<cnt_rows:

            mask_frame=frame.loc[mask_result==result.iat[cnt,0]]

            mask_time=mask_frame['date']
            mask=mask_frame.loc[mask_time>time]
            if not mask.empty:

                list.append(mask)
                cnt=cnt+1
            else:
                cnt=cnt+1
        return list
        


    def check_ip(self, frame):
        if frame.empty:
            return
        len_before=len(frame.index)
        tmp_ip=frame.iat[0,2]
        frame_ip=frame['ip_address']

        mask_frame_ip=frame.loc[frame_ip==tmp_ip]

        len_after=len(mask_frame_ip.index)

        if len_after==len_before:
            return True
        else:
            return  False


    def find_pair_ip(self, frame):

        frame_length=len(frame.index)
        cnt=0

        while frame_length-1>cnt:

            if frame.iat[cnt,2]==frame.iat[cnt+1,2]:
                cnt=cnt+1
            else:

                self.timedelta(frame.iat[cnt,0],frame.iat[cnt+1,0], frame.iloc[cnt,:], frame.iloc[cnt+1,:])
                cnt=cnt+1


    def find_ip(self,frame,level):
        open(self.result, 'w').close()

        mask_level=frame["level"]  # sort by method

        mask_level_=frame.loc[mask_level==level] #assign all stream with LEVEL from function as parameter

        mask_sid=mask_level_["sid"]   #mask for sid

        mask_drop_sid=mask_sid.drop_duplicates(keep='first', inplace=False)

        for sid in mask_drop_sid:               # use all
            if sid=="None":
                pass
            else:
                frame_sid = mask_level_.loc[mask_sid == sid]    # taking sid from frame

                if self.check_ip(frame_sid):
                    pass
                else:
                    self.find_pair_ip(frame_sid)# computing time between two ip address


    def find_ip_auto(self,frame, last_time):
        open(self.result, 'w').close()

        mask_sid=frame["sid"]   #mask for sid

        mask_drop_sid=mask_sid.drop_duplicates(keep='first', inplace=False)

        for sid in mask_drop_sid:               # use all
            if sid=="None":
                pass
            else:
                frame_sid = frame.loc[mask_sid == sid]    # taking sid from frame
                mask_time= frame_sid['date']
                frame_time=frame_sid.loc[mask_time>last_time]
                # print(frame_time)
                if self.check_ip(frame_time):
                    pass
                else:
                    self.find_pair_ip(frame_time)# computing time between two ip address

    def read_routes(self):

        try:
            def convert(val):

                return val
        except Exception as err:
            print(err)

        df = pd.read_csv(self.path_routes,delim_whitespace=True,
                         encoding='utf-8',
                         names=["routes"],
                         usecols=["routes"],
                         engine='python',
                         converters={'routes': convert},
                         )
        return df

    def add_route(self, route):

        with open(self.path_routes, 'a') as file:
            file.write("\n")
            file.write(route)
            file.close()
        # routes=self.read_routes()
        # print(routes)

    def show(self):
        return str(self.read_routes())


    def delete_route(self, route):

        result=self.read_routes()
        mask=result['routes']
        result_=result.loc[mask==route]

        if not result_.empty:
            result.drop(index=result_.index, inplace=True)
            open(self.file_name_routes, 'w').close()
            if not result.empty:

                with open(self.file_name_routes, 'w') as out:
                    out.write(result.to_string(header=False, index=False) )
                    out.close()
            return True
        else:
            return False



