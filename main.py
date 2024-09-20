from secret import authorization  # Import local discord authorization token

from time import sleep  # Import sleep from time library
import requests  # Import requests library


def main(headers, channel_id, user_id):

    params = {
        "limit": 100  # How many messages to get (max 100)
    }

    before_message_id = None

    while True:
        sleep(1)
        print(f"[+] LOADING | Trying to get {params['limit']} messages...")

        if before_message_id:  # If before_message_id is not None then gets older messages
            params["before"] = before_message_id

        # Gets the messages
        res = requests.get(f"https://discord.com/api/v10/channels/{channel_id}/messages", headers=headers, params=params)

        # Function to delete the messages
        if res.status_code == 200:
            messages = res.json()
            if len(messages) > 0:  # Checks if any messages left
                print(f"[+] LOADED | Got {len(messages)} messages! Checking every message...")
                for message in messages:  # For loop that iterates over each message
                    if user_id == message["author"]["id"]:  # Checks if it's your message
                        print(f"[+] DELETING | {message['author']['username']}: {message['content']}")

                        message_id = message["id"]

                        url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}"
                        res = requests.delete(url, headers=headers)  # Delete the message

                        if res.status_code == 204:  # If response status code is 204 (if success) print message below
                            print(f"[+] DELETED | Message (ID: {message_id}) from channel (ID: {channel_id})!")
                        else:  # If response status is not 204 (if not success) print message below
                            print(f"[!] ERROR | Message (ID: {message_id}) from channel (ID: {channel_id}) wasn't deleted! Reason: {res.text}")
                        sleep(0.5)  # Sleep 0.5 second to avoid request limit
                try:
                    before_message_id = messages[-1]["id"]  # Gets the last message id
                except IndexError:
                    pass
            else:
                break
        else:
            break
    print("[+] DONE")


if __name__ == "__main__":
    headers = {
        "authorization": authorization  # Define headers with your discord authorization token
    }

    channel_id = input("[?] Enter channel id here: ")
    user_id = input("[?] Enter your user id: ")

    # Gets the messages from a desired channel and then deletes them
    try:
        main(headers, channel_id, user_id)
    except KeyboardInterrupt:
        print("[!] Ctrl + C detected, terminating.")
