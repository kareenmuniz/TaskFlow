def payload(**overrides):
    data = {"title": "Estudar Flask", "description": "Revisar rotas", "priority": "Alta", "due_date": "2026-12-10"}
    data.update(overrides)
    return data

def test_create_and_list_task(client):
    response = client.post("/tasks/new", data=payload(), follow_redirects=True)
    assert response.status_code == 200
    assert b"Estudar Flask" in response.data
    assert b"Tarefa cadastrada com sucesso" in response.data

def test_reject_empty_title(client):
    response = client.post("/tasks/new", data=payload(title=""))
    assert response.status_code == 400
    assert "O título é obrigatório".encode() in response.data

def test_reject_invalid_priority(client):
    response = client.post("/tasks/new", data=payload(priority="Urgente"))
    assert response.status_code == 400
    assert "prioridade válida".encode() in response.data

def test_edit_task(client):
    client.post("/tasks/new", data=payload())
    response = client.post("/tasks/1/edit", data=payload(title="Título alterado"), follow_redirects=True)
    assert response.status_code == 200
    assert b"T\xc3\xadtulo alterado" in response.data

def test_toggle_status(client):
    client.post("/tasks/new", data=payload())
    response = client.post("/tasks/1/toggle", follow_redirects=True)
    assert response.status_code == 200
    assert b"Conclu\xc3\xadda" in response.data

def test_delete_task(client):
    client.post("/tasks/new", data=payload())
    response = client.post("/tasks/1/delete", follow_redirects=True)
    assert response.status_code == 200
    assert b"Estudar Flask" not in response.data

def test_missing_task_returns_404(client):
    assert client.get("/tasks/999/edit").status_code == 404
    assert client.post("/tasks/999/delete").status_code == 404

def test_filter_by_status(client):
    client.post("/tasks/new", data=payload())
    client.post("/tasks/1/toggle")
    response = client.get("/?status=Conclu%C3%ADda")
    assert response.status_code == 200
    assert b"Estudar Flask" in response.data
