from flask import Flask, request, jsonify
from models.task import Task
app = Flask(__name__)

tasks = []
id_tasks_control = 0

@app.route("/tasks", methods=["POST"])
def create_task():
    global id_tasks_control #Para utilizar a variável que foi declarada fora da função
    data = request.get_json()
    id_tasks_control += 1
    new_task = Task(id=id_tasks_control, title=data["title"], description=data.get("description", ""))
    tasks.append(new_task)
    return jsonify({"message": "Nova tarefa criada com sucesso"})

@app.route("/tasks", methods=["GET"])
def read_tasks():
    total_tasks = [task.to_dic() for task in tasks]

    output = {
        "tasks": total_tasks,
        "total_tasks": len(total_tasks)
    }
    return jsonify(output)

@app.route("/tasks/<int:id>", methods=["GET"])
def read_task_by_id(id):
    for task in tasks:
        if task.id == id:
            my_task = task
            return jsonify(my_task)
        
    return jsonify({"message": "Tarefa não existente"}), 404

@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    updated_task = request.get_json()
    for task in tasks:
        if task.id == id:
            task.title = updated_task["title"]
            task.description = updated_task["description"]
            task.completed = updated_task["completed"]
            return jsonify({"message": "Tarefa alterada com sucesso"})
        
    return jsonify({"message": "Tarefa não existente"}), 404

@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    for task in tasks:
        if task.id == id:
            tasks.remove(task)
            return jsonify({"message": "Tarefa excluída com sucesso"})
        
    return jsonify({"message": "Tarefa não existente"}), 404

if __name__ == "__main__":
    app.run(debug=True)