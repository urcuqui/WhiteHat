import pwd
import grp

def list_users():
    users = pwd.getpwall()
    
    for user in users:
        username = user.pw_name
        uid = user.pw_uid
        gid = user.pw_gid
        
        try:
            group = grp.getgrgid(gid).gr_name
        except KeyError:
            group = "Unknown"
        
        print(f"User: {username}")
        print(f"  UID: {uid}")
        print(f"  Primary Group: {group}")
        print("-" * 40)

if __name__ == "__main__":
    list_users()
