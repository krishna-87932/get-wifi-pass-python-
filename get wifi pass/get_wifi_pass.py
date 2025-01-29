import subprocess

def get_saved_wifi_passwords():
    try:
        # Get the list of saved Wi-Fi profiles
        profiles_output = subprocess.check_output("netsh wlan show profiles", shell=True, text=True)
        profiles = [line.split(":")[1].strip() for line in profiles_output.splitlines() if "All User Profile" in line]
        
        wifi_credentials = {}
        
        for profile in profiles:
            try:
                # Get the Wi-Fi profile details including the password
                profile_info = subprocess.check_output(f"netsh wlan show profile name=\"{profile}\" key=clear", shell=True, text=True)
                for line in profile_info.splitlines():
                    if "Key Content" in line:
                        password = line.split(":")[1].strip()
                        wifi_credentials[profile] = password
                        break
                else:
                    wifi_credentials[profile] = "No password found"
            except subprocess.CalledProcessError:
                wifi_credentials[profile] = "Error retrieving password"
        
        return wifi_credentials
    except Exception as e:
        print(f"Error: {e}")
        return {}

# Get and display the Wi-Fi names and passwords
wifi_passwords = get_saved_wifi_passwords()
with open("geted_wifi_pass.txt", 'w') as f:
    f.write(str(wifi_passwords))
if wifi_passwords:
    for wifi, password in wifi_passwords.items():
        print(f"Wi-Fi Name: {wifi}\nPassword: {password}\n")
else:
    print("No Wi-Fi networks found or access denied.")
