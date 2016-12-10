from flask import Flask, jsonify, abort, make_response, request;

app = Flask(__name__);

tasks = [ 
    { 'id': 1, 
     'title': u'Buy groceries',
     'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
     'done': False 
     },
    { 'id': 2,
     'title': u'Learn Python', 
     'description': u'Need to find a good Python tutorial on the web', 
     'done': False
     } 
     ]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404);

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks});

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET']) 
def get_task(task_id): 
    task = filter(lambda t: t['id'] == task_id, tasks)
    task = list(task);
    if len(task) == 0: 
        abort(404);
    print("====");
    return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks', methods=['POST']) 
def create_task(): 
    if not request.json or not 'title' in request.json:
        abort(400) 
    task = { 
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""), 
        'done': False
        } 
    tasks.append(task) 
    # 201 表示 'Created'
    return jsonify({'task': task}), 201

# curl -i -H "Content-Type: application/json" -X PUT -d '{"done":true}' http://localhost:5000/todo/api/v1.0/tasks/2
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT']) 
def update_task(task_id):
    print("=====");
    print(request.json);
    print(type(request.json['title']));
    print("=====");
    task = filter(lambda t: t['id'] == task_id, tasks) 
    task = list(task);
    if len(task) == 0: 
        abort(404) 
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) != str:
        abort(400) 
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title']) 
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

# curl http://localhost:5000/tasks/1 -X DELETE -v
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE']) 
def delete_task(task_id): 
    task = filter(lambda t: t['id'] == task_id, tasks) 
    task = list(task);
    if len(task) == 0: 
        abort(404) 
    tasks.remove(task[0]) 
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True);