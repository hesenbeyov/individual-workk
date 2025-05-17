import json
import os
from typing import List, Dict, Any

class VotingSystem:
    def __init__(self):
        self.candidates: Dict[str, int] = {}
        self.voters: List[Dict[str, Any]] = []
        self.filename = "voting_data.json"
        self.load_data()

    def display_welcome(self):
        print("\n=== Simple Voting System ===")
        print("Welcome to the Voting System!")
        print("===========================\n")

    def display_menu(self):
        print("\nMain Menu:")
        print("1. Add Candidate")
        print("2. Register Voter")
        print("3. Cast Vote")
        print("4. View All Candidates")
        print("5. View All Voters")
        print("6. Search Voter")
        print("7. Update Voter Information")
        print("8. Delete Voter")
        print("9. View Voting Statistics")
        print("10. Sort Candidates by Votes")
        print("11. Help")
        print("12. Clear All Data")
        print("13. Exit")
        return self.get_valid_input("Enter your choice (1-13): ", 1, 13)

    def get_valid_input(self, prompt: str, min_val: int, max_val: int) -> int:
        while True:
            try:
                choice = int(input(prompt))
                if min_val <= choice <= max_val:
                    return choice
                print(f"Please enter a number between {min_val} and {max_val}")
            except ValueError:
                print("Please enter a valid number")

    def add_candidate(self):
        name = input("Enter candidate name: ").strip()
        if name in self.candidates:
            print("Candidate already exists!")
            return
        self.candidates[name] = 0
        print(f"Candidate {name} added successfully!")
        self.save_data()

    def register_voter(self):
        voter_id = input("Enter voter ID: ").strip()
        if any(voter["id"] == voter_id for voter in self.voters):
            print("Voter ID already exists!")
            return
        name = input("Enter voter name: ").strip()
        self.voters.append({"id": voter_id, "name": name, "has_voted": False})
        print("Voter registered successfully!")
        self.save_data()

    def cast_vote(self):
        voter_id = input("Enter your voter ID: ").strip()
        voter = next((v for v in self.voters if v["id"] == voter_id), None)
        
        if not voter:
            print("Voter not found!")
            return
        if voter["has_voted"]:
            print("You have already voted!")
            return

        print("\nAvailable candidates:")
        for i, candidate in enumerate(self.candidates.keys(), 1):
            print(f"{i}. {candidate}")

        choice = self.get_valid_input("Enter candidate number: ", 1, len(self.candidates))
        candidate = list(self.candidates.keys())[choice - 1]
        self.candidates[candidate] += 1
        voter["has_voted"] = True
        print("Vote cast successfully!")
        self.save_data()

    def view_candidates(self):
        if not self.candidates:
            print("No candidates registered!")
            return
        print("\nCandidates and their votes:")
        for candidate, votes in self.candidates.items():
            print(f"{candidate}: {votes} votes")

    def view_voters(self):
        if not self.voters:
            print("No voters registered!")
            return
        print("\nRegistered Voters:")
        for voter in self.voters:
            print(f"ID: {voter['id']}, Name: {voter['name']}, Voted: {voter['has_voted']}")

    def search_voter(self):
        voter_id = input("Enter voter ID to search: ").strip()
        voter = next((v for v in self.voters if v["id"] == voter_id), None)
        if voter:
            print(f"\nVoter found:")
            print(f"ID: {voter['id']}")
            print(f"Name: {voter['name']}")
            print(f"Voted: {voter['has_voted']}")
        else:
            print("Voter not found!")

    def update_voter(self):
        voter_id = input("Enter voter ID to update: ").strip()
        voter = next((v for v in self.voters if v["id"] == voter_id), None)
        if not voter:
            print("Voter not found!")
            return
        new_name = input("Enter new name: ").strip()
        voter["name"] = new_name
        print("Voter information updated successfully!")
        self.save_data()

    def delete_voter(self):
        voter_id = input("Enter voter ID to delete: ").strip()
        for i, voter in enumerate(self.voters):
            if voter["id"] == voter_id:
                del self.voters[i]
                print("Voter deleted successfully!")
                self.save_data()
                return
        print("Voter not found!")

    def view_statistics(self):
        if not self.candidates:
            print("No voting data available!")
            return
        total_votes = sum(self.candidates.values())
        print("\nVoting Statistics:")
        print(f"Total votes cast: {total_votes}")
        print(f"Number of registered voters: {len(self.voters)}")
        print(f"Number of voters who have voted: {sum(1 for v in self.voters if v['has_voted'])}")
        if total_votes > 0:
            print("\nVote distribution:")
            for candidate, votes in self.candidates.items():
                percentage = (votes / total_votes) * 100
                print(f"{candidate}: {votes} votes ({percentage:.1f}%)")

    def sort_candidates(self):
        if not self.candidates:
            print("No candidates to sort!")
            return
        sorted_candidates = sorted(self.candidates.items(), key=lambda x: x[1], reverse=True)
        print("\nCandidates sorted by votes:")
        for candidate, votes in sorted_candidates:
            print(f"{candidate}: {votes} votes")

    def show_help(self):
        print("\nHelp Information:")
        print("1. Add Candidate: Register a new candidate for voting")
        print("2. Register Voter: Add a new voter to the system")
        print("3. Cast Vote: Record a vote for a candidate")
        print("4. View All Candidates: See all candidates and their vote counts")
        print("5. View All Voters: See all registered voters")
        print("6. Search Voter: Find a specific voter by ID")
        print("7. Update Voter: Modify voter information")
        print("8. Delete Voter: Remove a voter from the system")
        print("9. View Statistics: See voting statistics and percentages")
        print("10. Sort Candidates: View candidates sorted by vote count")
        print("11. Help: Show this help information")
        print("12. Clear Data: Remove all data from the system")
        print("13. Exit: Close the program")

    def clear_data(self):
        confirm = input("Are you sure you want to clear all data? (yes/no): ").lower()
        if confirm == "yes":
            self.candidates.clear()
            self.voters.clear()
            print("All data cleared successfully!")
            self.save_data()
        else:
            print("Operation cancelled.")

    def save_data(self):
        data = {
            "candidates": self.candidates,
            "voters": self.voters
        }
        try:
            with open(self.filename, "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_data(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, "r") as f:
                    data = json.load(f)
                    self.candidates = data["candidates"]
                    self.voters = data["voters"]
        except Exception as e:
            print(f"Error loading data: {e}")

    def run(self):
        self.display_welcome()
        while True:
            choice = self.display_menu()
            if choice == 1:
                self.add_candidate()
            elif choice == 2:
                self.register_voter()
            elif choice == 3:
                self.cast_vote()
            elif choice == 4:
                self.view_candidates()
            elif choice == 5:
                self.view_voters()
            elif choice == 6:
                self.search_voter()
            elif choice == 7:
                self.update_voter()
            elif choice == 8:
                self.delete_voter()
            elif choice == 9:
                self.view_statistics()
            elif choice == 10:
                self.sort_candidates()
            elif choice == 11:
                self.show_help()
            elif choice == 12:
                self.clear_data()
            elif choice == 13:
                print("\nThank you for using the Voting System!")
                break

if __name__ == "__main__":
    voting_system = VotingSystem()
    voting_system.run()
