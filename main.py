#BY BELAL STARTED AT 7:00AM 16/1/2021


import requests, json, colorama
from time import sleep
from colorama import Fore, Style
import getpass

colorama.init()

class InstagramUnfollow:
    
    print(Fore.BLUE +Style.BRIGHT+ f"""
    ╭╾──────────────────────────────╼╮
    │  Instagram Followings Cleaner  │
    │               Ω                │
    ╰╾──────────────────────────────╼╯
    
    """+ Fore.RESET)
    def __init__(self):
        self.headers = {
		"Accept": "*/*",
		"Accept-Encoding": "gzip, deflate",
		"Accept-Language": "en-US",
		"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 126.0.0.13.120 (iPhone10,5; iOS 13_3; en_US; en-US; scale=2.61; 1080x1920; 194985111)",
		"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
		"X-IG-Capabilities": "3brTvw==",
		"X-IG-Connection-Type": "WIFI",
		}
        self.session = requests.session()
        self.url = "https://i.instagram.com"
        self.API = "https://i.instagram.com/api/v1"
        self.allFollowingsPublic = []
        self.allFollowingsPrivate = []
        
    def Start(self):
        
        self.get_csrf()
        self.Login()

    def get_csrf(self):
        try:
            self.session.headers = self.headers
            self.session.headers.update({'Referer': self.url})
            getcsrf = self.session.get(self.url)
            self.csrf = getcsrf.cookies['csrftoken']
            self.session.headers.update({'X-CSRFToken': self.csrf})
        except Exception as e:
            print(Fore.RED + f'\r      Unknown Error.{Fore.RESET}')
        except KeyboardInterrupt:
            print(Fore.RED + f'\r      Process has been cancelled{Fore.RESET}')

    def Login(self):
        ASK = True
        try:
            while ASK:
                print(f"     {Fore.MAGENTA}Username      :      {Fore.RESET}", end='')
                username = input("")
                print(f"     {Fore.MAGENTA}Password      :      {Fore.RESET}", end='')
                password = getpass.getpass("")
                print("\n")
                self.account = self.session.post(self.url + "/accounts/login/ajax/", data={"username":username,"password":password}, allow_redirects=True)
                self.LoginData = self.account.json()
                if self.account.status_code != 200:
                    print(f'{Fore.RED}     authenticated.{Fore.RESET}', end='\n')
                elif self.LoginData['authenticated'] == True:
                    ASK = False

                elif self.LoginData['authenticated'] == False:
                    print(f"{Fore.RED}     username or password is wrong.{Fore.RESET}")

        except Exception as e:
            print(Fore.RED + f'\r     Unknown Error. {Fore.RESET}')
        except KeyboardInterrupt:
            try:
                print("\r     Press Enter to exit                                                                                                                                 ")
                input()
                exit()
            except KeyboardInterrupt:
                exit()

        self.get_followings()

    def get_followings(self):
        try:
            followings = self.session.get(self.API+'/friendships/'+ self.LoginData['userId'] +'/following/?rank_token={1}')
            self.followings_data = followings.json()
            for following in range(len(self.followings_data['users'])):
                if self.followings_data['users'][following]['is_private'] == True:
                    self.allFollowingsPrivate.append(self.followings_data['users'][following]['pk'])
                else:
                    self.allFollowingsPublic.append(self.followings_data['users'][following]['pk'])

            self.allFollowings = self.allFollowingsPublic + self.allFollowingsPrivate


            if followings.status_code == 200:
                userData = self.session.get(f"{self.API}/users/{self.LoginData['userId']}/info/")
                self.userFollowings = userData.json()['user']["following_count"]
                if self.userFollowings == 0:
                    print(f'\r                 {Fore.GREEN}You don\'t have any followings.{Fore.RESET}\n')
                if userData.status_code != 200:
                    self.userFollowings = 'unknown'
                else:
                    print(f'\r     {Fore.GREEN}User Followings: {int(self.userFollowings)}        Private:   {int(len(self.allFollowingsPrivate))-1}{Fore.RESET}\n')

            else:
                print(f"\r     {Fore.RED}There was an error getting followings.{Fore.RESET}")

        except Exception as e:
            print(Fore.RED + f'\r     Unknown Error. {Fore.RESET}')
        except KeyboardInterrupt:
            try:
                print("\r     Press Enter to exit                                                                                                                                 ")
                input()
                exit()
            except KeyboardInterrupt:
                exit()

        self.questions()


    def questions(self):
        try:
            questionKeepPrivate = print(f'     {Fore.YELLOW}Do you want to keep private accounts? (Y/N): {Fore.RESET}',end='')
            answer = input("")
            
            if answer == 'y' or answer == 'Y':
                self.keepPrivate = True        
            else:
                self.keepPrivate = False
            


        except Exception as e:
            print(Fore.RED + f'\r     Unknown Error.',e, f' {Fore.RESET}')
        except KeyboardInterrupt:
            try:
                print("\r     Press Enter to exit                                                                                                                                 ")
                input()
                exit()
            except KeyboardInterrupt:
                exit()

        self.unFollow()
    
    def unFollow(self):
        self.get_csrf()
        unfollowed = 1
        print('\n')
        try:                
            if self.keepPrivate:
                if self.allFollowingsPublic == [] and self.allFollowingsPrivate != []:
                    print(f"""\r     {Fore.YELLOW}         You Only have private followings,\n 
     Press enter to remove all followings including private.\n {Fore.RESET}""")
                    input()
                    print('\n')
                    for following in self.allFollowingsPrivate:
                        unfollowAction = self.session.post("https://www.instagram.com/web/friendships/"+str(following)+"/unfollow/", headers=self.headers)
                        sleep(0.5)
                        print(f'                        {Fore.GREEN}[{unfollowed}  /  {self.userFollowings}] {Fore.RESET}', end='\r')
                        unfollowed += 1
                
                for following in self.allFollowingsPublic:
                    unfollowAction = self.session.post("https://www.instagram.com/web/friendships/"+str(following)+"/unfollow/", headers=self.headers)
                    sleep(0.5)
                    print(f'                        {Fore.GREEN}[{unfollowed}  /  {self.userFollowings}] {Fore.RESET}', end='\r')
                    unfollowed += 1
            else:
                for following in self.allFollowings:
                    unfollowAction = self.session.post("https://www.instagram.com/web/friendships/"+str(following)+"/unfollow/", headers=self.headers)
                    print(f'\r                        {Fore.GREEN}[{unfollowed}  /  {self.userFollowings}] {Fore.RESET}', end='\r')
                    unfollowed += 1
            
            print(f'\r    {Fore.GREEN} You have unfollowed {unfollowed-1}.                                             {Fore.RESET}')
        
        except Exception as e:
            print(Fore.RED + f'\r     Unknown Error. {Fore.RESET}')
        except KeyboardInterrupt:
            try:
                print("\r     Press Enter to exit                                                                                      ")
                input()
                exit()
            except KeyboardInterrupt:
                exit()            


if __name__ == '__main__':
    InstagramBot = InstagramUnfollow()
    InstagramBot.Start()