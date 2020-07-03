#!/usr/bin/python3
import requests
import sys
from threading import Thread

def abort(msg):
    sys.exit(msg)

def fetch():
    global data1, data2
    api1 = requests.get("https://api.covid19india.org/v2/state_district_wise.json")
    api2 = requests.get("https://api.covid19india.org/v3/data.json")

    data1 = api1.json()
    data2 = api2.json()

def print_paramters(data):
    active = data.get('active') if data.get('active') else 'NA'
    confirmed = data.get('confirmed') if data.get('confirmed') else 'NA'
    recovered = data.get('recovered') if data.get('recovered') else 'NA'
    deceased = data.get('deceased') if data.get('deceased') else 'NA'
    tested = data.get('tested') if data.get('tested') else 'NA'

    print(f"\nACTIVE cases : {active}\nTESTED cases : {tested}\nCONFIRMED cases : {confirmed}\nRECOVERED cases : {recovered}\nDECEASED cases : {deceased}\n")

if __name__ == '__main__':
    # GET data from API:
    data1 = None
    data2 = None
    t = Thread(target=fetch)
    t.start()

    # Get input from user:
    state = input("Enter the state name\n> ").lower()
    district = input("Enter the district name\n> ").lower()
    if t.is_alive():
        t.join()

    # Filter state data:
    states = [data1.index(x) for x in data1 if state in x['state'].lower()]

    if len(states) == 0:
        abort('No such state found!')
    
    for st in states:
        state_code = data1[st]['statecode']
        print(f"\n*** STATE NAME : {data1[st]['state']} ***")
        state_data = data2[state_code].get('total')
        
        if state_data:
            print_paramters(state_data)
            districts_data = data1[st]['districtData']
            districts = [districts_data.index(x) for x in districts_data if district in x['district'].lower()]

            for dist in districts:
                district_data = districts_data[dist]
                print(f"\n{districts.index(dist)+1}) DISTRICT NAME: {district_data['district']}")
                print_paramters(district_data)
        else:
            pass
