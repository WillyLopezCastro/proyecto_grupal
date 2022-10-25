import os
from flask import flash, jsonify, redirect, send_from_directory, session, render_template, request, url_for
from flask_app import app
from flask_app.models.noticia import Noticia
from werkzeug.utils import secure_filename
from flask_app.utils.utils import allowed_file, agregar_codigo

@app.route('/noticias')
def noticias():
    if 'usuario_id' not in session:
        return redirect('/login')
    return render_template('noticias.html', all_noticias = Noticia.get_all_with_users())

@app.route('/noticias/new')
def new_noticia():
    if 'usuario_id' not in session:
        return redirect('/login')
    return render_template('crear_noticia.html')

@app.route('/procesar_noticia', methods=['POST'])
def procesar_noticia():
    print(request.form)
    if not Noticia.validar(request.form):
        return redirect('/noticias/new')
            # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part','error')
        return redirect('/noticias/new')
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect('/noticias/new')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = agregar_codigo(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_noticia = {
            'titulo': request.form['titulo'],
            'parrafo': request.form['parrafo'],
            'file': filename,
            'date_made': request.form['date_made'],
            'usuario_id': session['usuario_id']
        }
        noticia = Noticia.save(new_noticia)
        flash("Noticia creada", "success")

        if noticia == False:
            flash('Al malo pasó al crear la noticia', 'error')
            return redirect('/noticias/new')
        return redirect('/noticias')

@app.route('/noticias/edit/<int:id>')
def edit_noticia(id):
    if 'usuario_id' not in session:
        return redirect('/noticias')
    noticia = Noticia.get_by_id_with_users(id)[0]
    if session['usuario_id'] == noticia.usuario_id:
        noticia.date_made = noticia.date_made.strftime("%Y-%m-%d")
        return render_template('editar_noticia.html', noticia=noticia)
    return redirect(f'/noticias/{id}')

@app.route('/process/edit/noticia/<int:id>', methods=['POST'])
def process_edit_noticia(id):
    if not Noticia.validar(request.form):
        return redirect(f'/noticias/edit/{id}')
            # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part','error')
        return redirect(f'/noticias/edit/{id}')
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(f'/noticias/edit/{id}')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = agregar_codigo(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        edit_noticia = {
            'id': id,
            'titulo': request.form['titulo'],
            'parrafo': request.form['parrafo'],
            'file': filename,
            'date_made': request.form['date_made'],
        }
        updated = Noticia.update(edit_noticia)
        flash("Noticia editada", "success")
        return redirect('/noticias')
    flash('No se guardó la imagen, el archivo no está permitido', 'error')
    return redirect(f'/noticias/edit/{id}')



@app.route('/noticias/<int:id>')
def view_noticias(id):
    noticia = Noticia.get_by_id_with_users(id)[0]
    noticia.date_made = noticia.date_made.strftime("%Y-%m-%d")
    return render_template('about.html', noticia = noticia)

@app.route('/noticias/delete/<int:id>')
def delete_noticias(id):
    if 'usuario_id' not in session:
        return redirect('/noticias')
    noticia = Noticia.get_by_id_with_users(id)[0]
    if session['usuario_id'] == noticia.usuario_id:
        noticia = Noticia.delete(id)
        flash("Noticia eliminada", "success")
        return redirect('/noticias')
    return redirect('/noticias')


#FOTOS
@app.route("/noticias/fotos/<id>")
def noticias_fotos(id):
    return render_template('noticias/noticias_fotos.html', noticia=Noticia.get_by_id_with_users(id))

@app.route('/noticias/fotos/subir/<id>', methods=['POST'])
def upload_foto(id):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part','error')
            return redirect(f'/noticias/fotos/{id}')
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(f'/noticias/fotos/{id}')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))    

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)