from datetime import date

class ValidationError(ValueError):
    pass

class TaskService:
    PRIORITIES = {"Baixa", "Média", "Alta"}

    def __init__(self, repository):
        self.repository = repository

    def _validate(self, form):
        title = (form.get("title") or "").strip()
        description = (form.get("description") or "").strip()
        priority = (form.get("priority") or "Média").strip()
        due_date = (form.get("due_date") or "").strip() or None
        if not title:
            raise ValidationError("O título é obrigatório.")
        if len(title) > 120:
            raise ValidationError("O título deve ter no máximo 120 caracteres.")
        if len(description) > 1000:
            raise ValidationError("A descrição deve ter no máximo 1.000 caracteres.")
        if priority not in self.PRIORITIES:
            raise ValidationError("Selecione uma prioridade válida.")
        if due_date:
            try:
                date.fromisoformat(due_date)
            except ValueError:
                raise ValidationError("Informe uma data válida.")
        return {"title": title, "description": description,
                "priority": priority, "due_date": due_date}

    def create_task(self, form):
        return self.repository.insert(self._validate(form))

    def update_task(self, task_id, form):
        return self.repository.update(task_id, self._validate(form))

    def list_tasks(self, status=None):
        return self.repository.list_all(status)

    def get_task(self, task_id):
        return self.repository.get(task_id)

    def delete_task(self, task_id):
        return self.repository.delete(task_id)

    def toggle_status(self, task_id):
        task = self.repository.get(task_id)
        if not task:
            return False
        new_status = "Pendente" if task["status"] == "Concluída" else "Concluída"
        return self.repository.set_status(task_id, new_status)

    def count_by_status(self):
        return self.repository.counts()
