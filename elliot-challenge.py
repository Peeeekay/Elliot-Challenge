
from datetime import datetime
from operator import itemgetter

#storing the daya in hash
#day_hash = {"date":[(startTime,endtime),(startTime,endTime)....],"next_day": ...}
day_hash = {}
busy_time_hash = {}

import CSV

def extract_data():
    with open('calender.csv','rb') as f:
        reader = csv.reader(f)
        temp_data = []
        for row in reader:
            temp_data= row.split(',')
            extract_date_start = temp_data[0]
            extract_date_end = temp_data[1]
            #Assumption that the event does not take more than a day/
            datetime_object_start = datetime.strptime(extract_date_start, '%b %d %Y %I:%M%p')
            datetime_object_end = datetime.strptime(extract_date_end, '%b %d %Y %I:%M%p')

            date = datetime_object_start.date
            if date <= week_date and datetime_object_start.hour() >= datetime.time(8) and datetime_object_end.hour() <= datetime.time(22):
                if str(date) in day_hash:
                    hash_array = day_hash.get(str(date))
                    time_tuple = (datetime_object_start, datetime_object_end)
                    hash_array.append(time_tuple)
                else:
                    hash_array = []
                    time_tuple = (datetime_object_start, datetime_object_end)
                    hash_array.append(time_tuple)
                    day_hash.update({str(date):hash_array})




def get_time_info(key):
    return day_hash[key]

def test_overlap(start,end,time_array):
    #tests all the overlaps, and re arranges accodingly
    for cursor,time in enumerate(time_array):
        if start >= time[0]:
            if end >= time[1]:
                time_array[cursor][1] = end
                return True
    else:
        return False

def get_free_slot(time_array):
    #gets the maximum diff time
    temp_time=[]
    for i in range(len(time_array)-1):
        temp.append(time_array[i+1][0] - time_array[i][1])
        temp_time.append(time_array[i][1])

    max_diff = max(temp)
    max_index = temp.index(max_diff)
    return (temp_time[max_index],temp_time[max_index] + max_diff,max_diff)

def sort_arrays():
    for key in day_hash.keys():
        arr = day_hash[key]
        day_hash[key] = sorted(arr,key=itemgetter(1))

#runs the program
def main():
    today_date = datetime.now().date
    week_date = today_date + 7
    extract_data(week_date)
    sort_arrays()
    # creates the array of array while making the union of all the busy times.
    # the difference between the disjointed sets is the available free slot
    for key in day_hash.keys:
        if key not in busy_time_hash:
            busy_time_hash.update({key:[]})
        time_values = get_time_info(key)
        for time in time_values:
            time_array = busy_time_hash[key]
            if len(time_array) == 0:
                busy_arr = [time[0],time[1]]
                time_array.append(busy_arr)
            elif not test_overlap(time[0],time[1],time_array):
                busy_arr = [time[0],time[1]]
                time_array.append(busy_arr)

    maximum_array=[]
    #finds the maximum free slot in a week
    for key in day_hash.keys:
        time_array = busy_time_hash[key]
        maximum_array.append(get_free_slot(time_array))


    maximum_free_slot=max(maximum_array, key=lambda x:x[2])
    max_slot = maximum_array.index(maximum_free_slot)
    #returns the maxslot
    return (max_slot(0),max_slot(1))

main()









