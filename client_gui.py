import tkinter as tk
from tkinter import messagebox
import requests

# Flask server URL
SERVER_URL = 'http://127.0.0.1:5000'
session = requests.Session()
student_id = None

# ---- Login Function ----
def login():
    global student_id
    sid = entry_sid.get()
    password = entry_password.get()

    response = session.post(f"{SERVER_URL}/login", json={"student_id": sid, "password": password})

    if response.status_code == 200:
        student_id = sid
        messagebox.showinfo("Login", "Login successful!")
        login_window.withdraw()
        show_dashboard()
    else:
        messagebox.showerror("Login Failed", response.json().get("error", "Unknown error"))

# ---- Dashboard ----
def show_dashboard():
    dashboard_window.deiconify()
    proposal_listbox.delete(0, tk.END)

    response = session.get(f"{SERVER_URL}/proposals")
    if response.status_code == 200:
        proposals = response.json()
        for proposal in proposals:
            # Modify the display text to include the "Pitched By" information
            text = f"{proposal['ProposalID']}: {proposal['Title']} (Pitched By: {proposal['PitchedBy']})"
            proposal_listbox.insert(tk.END, text)
    else:
        messagebox.showerror("Error", "Failed to load proposals")


# ---- Cast Vote ----
def vote():
    selected = proposal_listbox.curselection()
    if not selected:
        messagebox.showwarning("Select Proposal", "Please select a proposal to vote for.")
        return

    proposal_id = int(proposal_listbox.get(selected[0]).split(":")[0])
    response = session.post(f"{SERVER_URL}/vote/{proposal_id}")

    if response.status_code == 200:
        messagebox.showinfo("Vote", "Vote recorded!")
    else:
        messagebox.showerror("Error", response.json().get("error", "Voting failed."))


# ---- Pitch Proposal Function ----
def pitch_proposal():
    def submit_pitch():
        title = entry_title.get()
        description = entry_description.get()

        if not title or not description:
            messagebox.showwarning("Missing Information", "Please provide both title and description.")
            return

        response = session.post(f"{SERVER_URL}/pitch", json={"title": title, "description": description})

        if response.status_code == 200:
            messagebox.showinfo("Proposal Pitched", "Your proposal has been successfully pitched!")
            pitch_window.destroy()
            show_dashboard()  # Refresh the dashboard to include the new proposal
        else:
            messagebox.showerror("Error", response.json().get("error", "Pitching failed."))

    pitch_window = tk.Toplevel(dashboard_window)
    pitch_window.title("Pitch Your Proposal")

    tk.Label(pitch_window, text="Proposal Title:").pack()
    entry_title = tk.Entry(pitch_window, width=40)
    entry_title.pack(pady=5)

    tk.Label(pitch_window, text="Description:").pack()
    entry_description = tk.Entry(pitch_window, width=40)
    entry_description.pack(pady=5)

    tk.Button(pitch_window, text="Submit", command=submit_pitch).pack(pady=10)
    pitch_window.mainloop()






# ---- GUI ----
login_window = tk.Tk()
login_window.title("Campus Voting Login")

tk.Label(login_window, text="Student ID:").pack()
entry_sid = tk.Entry(login_window)
entry_sid.pack()

tk.Label(login_window, text="Password:").pack()
entry_password = tk.Entry(login_window, show='*')
entry_password.pack()

tk.Button(login_window, text="Login", command=login).pack(pady=10)

dashboard_window = tk.Toplevel(login_window)
dashboard_window.title("Vote for Proposals")
dashboard_window.withdraw()

proposal_listbox = tk.Listbox(dashboard_window, width=50)
proposal_listbox.pack(pady=10)

vote_button = tk.Button(dashboard_window, text="Vote", command=vote)
vote_button.pack()

pitch_button = tk.Button(dashboard_window, text="Pitch Proposal", command=pitch_proposal)
pitch_button.pack(pady=10)

# Start the GUI
login_window.mainloop()

