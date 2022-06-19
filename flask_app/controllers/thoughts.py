from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.thought import Thought

@app.route('/thoughts')
def thoughts():
    return render_template('thought.html')

@app.route('/create/thought', methods=['POST'])
def create_thought():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Thought.validate_thought(request.form):
        return redirect('/thoughts')
    data = {
        "thought_content": request.form["thought_content"],
        'user_id': session['user_id']
    }
    Thought.save(data)
    return redirect('/')



@app.route('/thought/<int:id>')
def show_thought(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'thought_id' : id,
        'user_id': session['user_id']
    }
    myThought = Thought.get_one(data)
    return render_template('index.html', thought=myThought,  user=User.get_by_id(data))


@app.route('/thought/<int:id>/like', methods=['GET','PUT'])
def like_thought(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'thought_id': id,
        'user_id': session['user_id']
    }
    Thought.addLike(data)
    return redirect('/')


@app.route('/thought/<int:id>/unlike', methods=['GET','PUT'])
def unlike_thought(id):
    if 'user_id' not in session:
            return redirect('/logout')
    data={
        'thought_id': id,
        'user_id': session['user_id'],
    }
    Thought.removeLike(data)
    return redirect('/')


@app.route('/thought/destroy/<int:id>')
def delete_thought(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Thought.destroy(data)
    return redirect('/')

