from flask import Flask, render_template, request, redirect, url_for, flash, abort
from config import Config
from repository import TaskRepository
from services.task_service import TaskService, ValidationError

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    repository = TaskRepository(app.config["DATABASE"])
    service = TaskService(repository)
    app.extensions["task_service"] = service

    @app.get("/")
    def index():
        status = request.args.get("status", "")
        tasks = service.list_tasks(status=status or None)
        counts = service.count_by_status()
        return render_template("index.html", tasks=tasks, counts=counts, current_status=status)

    @app.route("/tasks/new", methods=["GET", "POST"])
    def create_task():
        if request.method == "POST":
            try:
                service.create_task(request.form)
                flash("Tarefa cadastrada com sucesso.", "success")
                return redirect(url_for("index"))
            except ValidationError as exc:
                flash(str(exc), "error")
                return render_template("form.html", task=request.form, page_title="Nova tarefa"), 400
        return render_template("form.html", task={}, page_title="Nova tarefa")

    @app.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
    def edit_task(task_id):
        task = service.get_task(task_id)
        if task is None:
            abort(404)
        if request.method == "POST":
            try:
                service.update_task(task_id, request.form)
                flash("Tarefa atualizada com sucesso.", "success")
                return redirect(url_for("index"))
            except ValidationError as exc:
                flash(str(exc), "error")
                return render_template("form.html", task={**task, **request.form}, page_title="Editar tarefa"), 400
        return render_template("form.html", task=task, page_title="Editar tarefa")

    @app.post("/tasks/<int:task_id>/delete")
    def delete_task(task_id):
        if not service.delete_task(task_id):
            abort(404)
        flash("Tarefa excluída.", "success")
        return redirect(url_for("index"))

    @app.post("/tasks/<int:task_id>/toggle")
    def toggle_task(task_id):
        if not service.toggle_status(task_id):
            abort(404)
        flash("Status atualizado.", "success")
        return redirect(url_for("index"))

    return app

if __name__ == "__main__":
    create_app().run(debug=False)
