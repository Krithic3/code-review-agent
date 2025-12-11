Code Review Mini-Agent – Workflow Engine (FastAPI)
This project is my submission for the AI Engineering Internship Coding Assignment.
It implements a minimal agent workflow engine similar to a simplified LangGraph, using FastAPI.

🚀 Features Implemented
1. Workflow / Graph Engine
Nodes = Python functions that read & update shared state
State flows from one node to the next
Edges define execution order
Looping supported (repeat nodes until condition met)
Conditional logic supported via state values
Clean, simple, modular design

2. Tool Registry
A simple registry that allows nodes to call named functions.
Example tools implemented:
Extract functions from code
Compute complexity
Detect issues
Generate suggestions

3. FastAPI Endpoints
Endpoint	Description
POST /graph/create	Creates a workflow graph
POST /graph/run	Runs the workflow with an initial state
GET /graph/state/{run_id}	Returns logs + final agent output
All endpoints tested and working

🤖 Example Workflow Implemented: Code Review Mini-Agent
This workflow performs:
Extract functions from Python code
Compute complexity for each function
Detect simple issues (print statements, eval, TODO, etc.)
Suggest improvements
Loop until quality_score >= threshold
Completely rule-based, no ML used.

🛠️ How to Run
1. Clone the repository
git clone https://github.com/Krithic3/code-review-agent.git
cd code-review-agent

2. Create a virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

3. Install dependencies
pip install -r requirements.txt

4. Start FastAPI server
uvicorn app.main:app --reload

5. Open the API docs
Navigate to:
http://127.0.0.1:8000/docs

You can now:
Create a graph
Run it with sample code
View execution logs and agent outputs

⭐ Possible Improvements (With More Time)
Add background workers for async long-running tasks
WebSocket log streaming for real-time execution
Graph persistence in SQLite/Postgres
Visual graph editor
Support for parallel node execution
Better static code analysis tools

📬 Final Notes
This project demonstrates:
Clean Python structure
Good FastAPI design
Clear reasoning about state → transitions → loops
Ability to build backend systems from scratch
Thank you for reviewing my submission!
