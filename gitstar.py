import requests
import json
import getpass

GITHUB_API_URL = "https://api.github.com/"

def check_credentials(username, password):
    try:
        response = requests.head(GITHUB_API_URL, auth=(username, password))
    except requests.exceptions.ConnectionError as e:
        print("Please check your internet connection!")
        exit()

    return response.ok

def star_repo(username, password, friendusername, repo_list, mode):
    for repo in repo_list:
        if 'name' in repo:  # Check if 'name' key exists in the repo dictionary
            repo_name = repo['name']
            url = GITHUB_API_URL + "user/starred/" + friendusername + "/" + repo_name

            if not repo['fork']:
                print(repo_name)
                if mode:
                    requests.put(url, auth=(username, password))
                else:
                    requests.delete(url, auth=(username, password))

def main():
    _username = input("Username for 'https://github.com': ")
    _password = getpass.getpass("Password for 'https://" + _username + "@github.com': ")

    if not check_credentials(_username, _password):
        print("Invalid Credentials. Please try again.")
        return
    else:
        print("Logged in Successfully.")
        _friendusername = input("Username of friend for which you want to star all the repos: ")

        # Update headers to include authentication
        headers = {
            "Authorization": "token " + _password  # Assuming password is your GitHub personal access token
        }
        
        url = GITHUB_API_URL + "users/" + _friendusername + "/repos?per_page=100"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = json.loads(response.text)
            print("\nThe following repos are being starred: ")
            star_repo(_username, _password, _friendusername, data, True)

            _reverse = input("\n\nDo you want a reverse mechanism? (Y/N) ").lower()
            if _reverse in ['y', 'yes']:
                print("\nThe following repos are being un-starred: ")
                star_repo(_username, _password, _friendusername, data, False)

            print("\n\nThat was a great thing you did for your friend!")
        else:
            print("Failed to fetch repository data. Status code:", response.status_code)

if __name__ == "__main__":
    main()

