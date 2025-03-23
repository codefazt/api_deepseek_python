import requests
import argparse
import threading
import subprocess
import time

# CLEAR CMD FUNCTION --------------

def clean_cmd():
    # Command to clear the terminal output (replace with appropriate commands for other platforms)
    cmd = 'cls'
    try:
        process = subprocess.run(['cmd', '/c', cmd], text=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute command: {e}")
    
    # if process.returncode == 0:
    #     print("CMD window cleared successfully.")

def progress_loading(loading_status:str) -> str:

    if loading_status == "| [Loading.]":
        return "/ [Loading..]"
    
    if loading_status == "/ [Loading..]":
        return "- [Loading...]"
    
    if loading_status == "- [Loading...]":
        return "\\ [Loading....]"
    
    if loading_status == "\\ [Loading....]":
        return "| [Loading.]"

# LOADING FUNCTION --------------

is_loading = True
def loading():

    global is_loading
    counter = 0

    loading_status = "\\ [Loading....]"
    while is_loading:
        
        clean_cmd()
        loading_status = progress_loading(loading_status)
        print(loading_status)
        time.sleep(0.5)
        
        counter += 1
        if counter == 10000:
            is_loading = False
            print("\n[Loading Got an Error.]")
            exit(1)
     
# MAiN FUNCTION --------------
def main():

    global is_loading
           
    parser = argparse.ArgumentParser(description='A simple argument parsing example that saves arguments to a file.')
    parser.add_argument('--question', type=str, default=None,
                        help='Question to ask the model', required=True)

    args = parser.parse_args()

    # Configuration
    # API_KEY = "sk-f26f9c824b5c5cd1bf433589119667c5"
    API_ENDPOINT = "http://172.16.0.3:1234/v1/chat/completions"  # path of local deepseek endpoint

    headers = {
        # "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",  # Specify the model (e.g., deepseek-coder, deepseek-r1)
        "messages": [
            {"role": "user", "content": args.question}
        ],
        "temperature": 0.7
    }

    try:
        threading.Thread(target=loading).start()
        response = requests.post(API_ENDPOINT, json=payload, headers=headers)

        if response:
            is_loading = False

        response.raise_for_status()  # Raise HTTP errors
        data = response.json()

        print("Response:", data['choices'][0]['message']['content'])
        # print(data['choices'])
    except requests.exceptions.RequestException as e:
        print("Error:", e)

if __name__ == "__main__":
    main()