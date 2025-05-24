import requests
import sys
from rich import print as rich_print


def check_activity(user_name):
    response = requests.get(f"https://api.github.com/users/{user_name}/events")
    if response.status_code ==200:
        events = response.json()
        if not events:
                print(f"{user_name} has no recent activity")
        else:
            rich_print(f"github-activity[bold green]{user_name}[/bold green]:")

            for event in events:
                print(f"- {event['type']} at {event['created_at']}")
                event_type = event["type"]
                repo_name = event["repo"]["name"]
                payload = event["payload"]

                if event_type == "PushEvent":
                    commit_count = len(payload.get("commits", []))
                    print( f"- Pushed {commit_count} commit{'s' if commit_count != 1 else ''} to {repo_name}")
                
                elif event_type == "IssuesEvent" and payload["action"] == "opened":
                    print( f"- Opened a new issue in {repo_name}")
                
                elif event_type == "WatchEvent":
                    print( f"- Starred {repo_name}")
                else:
                    print(f"{event_type} on {repo_name}")
    else:
         print(f"failed to retrieve  activities for {user_name}. Status Code: {response.status_code}")

if __name__ == "__main__":

    if len(sys.argv) > 1:
        user_name = sys.argv[1]
    else:
        user_name = input("Enter the github user name: ")
    
    check_activity(user_name)
            



