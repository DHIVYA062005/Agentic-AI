import pandas as pd

def load_tasks(file_path='tasks_assigned.csv'):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print("Task file not found.")
        return pd.DataFrame()

def show_all_tasks(tasks_df):
    print("\n=== All Tasks ===")
    print(tasks_df.to_string(index=False))

def show_tasks_by_camera(tasks_df, camera_id):
    filtered = tasks_df[tasks_df['camera_id'].astype(str).str.contains(str(camera_id))]
    if not filtered.empty:
        print(f"\n=== Tasks for Camera {camera_id} ===")
        print(filtered.to_string(index=False))
    else:
        print(f"No tasks found for Camera {camera_id}")

def show_high_priority_tasks(tasks_df):
    filtered = tasks_df[tasks_df['priority'].str.lower() == 'high']
    if not filtered.empty:
        print("\n=== High Priority Tasks ===")
        print(filtered.to_string(index=False))
    else:
        print("No high priority tasks.")

def run_chatbot():
    print("🤖 Welcome to the Agentic AI Chatbot Assistant")
    tasks_df = load_tasks()

    if tasks_df.empty:
        return

    while True:
        user_input = input("\nAsk me something (type 'exit' to quit): ").lower()

        if 'exit' in user_input:
            print("Goodbye!")
            break
        elif 'all tasks' in user_input:
            show_all_tasks(tasks_df)
        elif 'camera' in user_input:
            cam_id = ''.join(filter(str.isdigit, user_input))
            show_tasks_by_camera(tasks_df, cam_id)
        elif 'high priority' in user_input:
            show_high_priority_tasks(tasks_df)
        else:
            print("I didn't understand that. Try asking: 'List all tasks', 'Tasks for camera 1', or 'High priority tasks'.")

if __name__ == '__main__':
    run_chatbot()
