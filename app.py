from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "secret-key"  # Required for flashing messages

# In-memory "database" (use SQLite or another DB for production)
notes = []

@app.route('/')
def index():
    query = request.args.get('query', '').lower()
    sort_by = request.args.get('sort_by')
    
    # Filter notes based on search query
    filtered_notes = [note for note in notes if query in note['title'].lower() or query in note['content'].lower()]
    
    # Sort notes based on selected sort option
    if sort_by == 'title':
        filtered_notes = sorted(filtered_notes, key=lambda x: x['title'].lower())
    elif sort_by == 'date':
        filtered_notes = sorted(filtered_notes, key=lambda x: x['id'])
    
    return render_template('index.html', notes=filtered_notes)

@app.route('/add', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note = {'id': len(notes) + 1, 'title': title, 'content': content}
        notes.append(note)
        flash('Note added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_note.html')

@app.route('/update/<int:note_id>', methods=['GET', 'POST'])
def update_note(note_id):
    note = next((note for note in notes if note['id'] == note_id), None)
    if not note:
        return "Note not found", 404
    if request.method == 'POST':
        note['title'] = request.form['title']
        note['content'] = request.form['content']
        flash('Note updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('update_note.html', note=note)

@app.route('/delete/<int:note_id>')
def delete_note(note_id):
    global notes
    notes = [note for note in notes if note['id'] != note_id]
    flash('Note deleted successfully!', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
