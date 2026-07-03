import subprocess
import os

def get_wifi_passwords():
    #1. ge the lsit of all saved wifi profiles 
    #we are runnin th command: netsh wlan show profiles
    meta_data= subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])

    #decode the weird windows text format
    data= meta_data.decode('utf-8', errors="ignore")
    data= data.split('\n')

    #Extract wifi names

    profiles = []
    for line in data:
        if " All User Profile"in line:
            #split the line to get the name apart
            #Line looks like : " ALL user profile : IPhone"
            parts= line.split(":")
            wifi_name= parts[1].strip()
            profiles.append(wifi_name)

        print(f"---FOUND {len(profiles)}SAVED NETWORKS---\n")

        #2. Loop through each wifi and get the password(with a counter)
        total=len(profiles)
        for i,name in enumerate(profiles, 1):
         print(f"[{i}/{total}]Checking...", end="\r")#Progress bar effectpy
         try:
                #The  magic comand: netsh wlan show profile name="X" key=clear
                results= subprocess.check_output(['netsh', 'wlan', 'show', 'profile' , name,'key=clear'])   
                results=results.decode('utf-8', errors="ignore")
                results=results.split('\n')

                #find the password line
                password=None
                for line in results:
                    if "Key Content" in line:
                        password = line.split(":")[1].strip()
                        break
                # print the result
                if password:
                    print(f"WIFI:{name:<20} | PASS:{password}") 
                else: 
                    print(f"WIFI:{name:<20}| [X](Open network/no pass)")
         except subprocess.CalledProcessError:
             print(f"WIFI:{name:<20} | (Error reading)")
#---RUN---
os.system('cls')
get_wifi_passwords()
input("\nPress Enter to exit...")                    
