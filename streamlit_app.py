import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import os

st.set_page_config(page_title="Agentic AI CCTV Task System", layout="wide")
st.title(" Agentic AI Task ")

LOG_FILE = "simulated_log.csv"
ASSIGN_FILE = "tasks_assigned.csv"

# Sample task pool
TASKS = [
    "Inspect site A",
    "Check equipment B",
    "Restock materials",
    "Clean up zone C",
    "Assist supervisor"
]

# --- Detect idle people and assign tasks ---
def detect_idle_and_assign(threshold_sec=60):
    if not os.path.exists(LOG_FILE):
        return [], pd.DataFrame()

    df = pd.read_csv(LOG_FILE)
    df["frame_time"] = df["frame"] / 10  # since fps=10 in simulate_cctv.py
    df = df.sort_values("frame_time", ascending=False)

    # Take latest entry per worker
    latest = df.groupby("worker_id").first().reset_index()

    # Mark idle workers
    idle_workers = latest[latest["status"] == "idle"]

    # Assign random tasks
    assignments = []
    for i, row in idle_workers.iterrows():
        task = TASKS[i % len(TASKS)]
        assignments.append({
            "worker_id": row["worker_id"],
            "task": task,
            "assigned_time": datetime.now().isoformat()
        })

    assigned_df = pd.DataFrame(assignments)
    if not assigned_df.empty:
        assigned_df.to_csv(ASSIGN_FILE, index=False)

    return idle_workers, assigned_df


# --- Streamlit Layout ---
st.sidebar.info("Uses CCTV logs to detect idle workers and assign tasks automatically.")

if st.button("📡 Detect Idle & Assign Task"):
    idle_df, assigned_df = detect_idle_and_assign()

    if not idle_df.empty:
        st.success(f"Detected {len(idle_df)} idle workers. Tasks assigned:")
        st.dataframe(assigned_df)
    else:
        st.info("No idle workers found.")

# Optional: View raw log or assigned file
st.markdown("### 📄 View Simulation Log")
if os.path.exists(LOG_FILE):
    sim_df = pd.read_csv(LOG_FILE)
    st.dataframe(sim_df.tail(100))
else:
    st.warning("Simulation log file not found.")

st.markdown("### ✅ View Assigned Tasks")
if os.path.exists(ASSIGN_FILE):
    assigned = pd.read_csv(ASSIGN_FILE)
    st.dataframe(assigned)
    st.download_button("Download Task Assignments", data=assigned.to_csv(index=False), file_name="tasks_assigned.csv", mime="text/csv")
else:
    st.info("No task assignments yet.")
# --- 💬 Chatbot Assistant ---
st.markdown("## 🤖 Chat with Task Assistant")

user_input = st.text_input("Ask about tasks (e.g., 'What is the task for worker 2?', 'Show all tasks', 'Any high priority tasks?')")

def interpret_query(query, df):
    query = query.lower()
    
    # Extract worker ID
    if 'worker' in query and any(char.isdigit() for char in query):
        worker_id = ''.join(filter(str.isdigit, query))
        filtered = df[df['worker_id'].astype(str) == worker_id]
        if not filtered.empty:
            return filtered
        else:
            return f"🚫 No task found for worker {worker_id}"

    # Show all tasks
    elif 'all tasks' in query or 'show tasks' in query or query.strip() == 'tasks':
        return df

    # High priority filter (if column exists)
    elif 'high priority' in query and 'priority' in df.columns:
        filtered = df[df['priority'].str.lower() == 'high']
        return filtered if not filtered.empty else "✅ No high priority tasks."

    # Camera ID based (if present in the dataset)
    elif 'camera' in query and 'camera_id' in df.columns:
        cam_id = ''.join(filter(str.isdigit, query))
        filtered = df[df['camera_id'].astype(str).str.contains(cam_id)]
        return filtered if not filtered.empty else f"🚫 No tasks found for camera {cam_id}"

    # Default fallback
    return "🤔 I couldn't understand that. Try: 'Show all tasks', 'Tasks for worker 2', 'High priority tasks'."

# Load tasks and respond
if user_input and os.path.exists(ASSIGN_FILE):
    df = pd.read_csv(ASSIGN_FILE)
    result = interpret_query(user_input, df)

    if isinstance(result, pd.DataFrame):
        if result.empty:
            st.warning("No matching records found.")
        else:
            st.dataframe(result)
    else:
        st.info(result)
