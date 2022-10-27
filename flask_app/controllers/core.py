from flask import redirect, render_template, request, flash, session
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_app.models.noticia import Noticia
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():

    all_noticias = Noticia.get_all_with_users()
    print(all_noticias)
    return render_template("categori.html", all_noticias = all_noticias)

@app.route("/login")
def login():

    if 'usuario' in session:
        flash('Ya estás LOGEADO!', 'warning')
        return redirect('/login')

    return render_template("login.html")

@app.route("/usuario/new")
def usuario_new():

    if 'usuario' in session:

        return render_template("crear_usuario.html")

    return redirect('/login')


@app.route("/procesar_registro", methods=["POST"])
def procesar_registro():

    if not Usuario.validar(request.form):
        return redirect('/login')

    pass_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        'nombre' : request.form['nombre'],
        'apellido' : request.form['apellido'],
        'email' : request.form['email'],
        'password' : pass_hash,
    }

    resultado = Usuario.save(data)

    if not resultado:
        flash("error al crear el usuario", "error")
        return redirect("/usuario/new")

    flash("Usuario creado correctamente", "success")
    return redirect("/noticias")


@app.route("/procesar_login", methods=["POST"])
def procesar_login():

    usuario = Usuario.buscar(request.form['identificacion'])

    if not usuario:
        flash("Correo/Clave Invalidas", "error")
        return redirect("/login")

    if not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("Correo/Clave Invalidas", "error")
        return redirect("/login")

    session['usuario'] = usuario.nombre
    session['usuario_id'] = usuario.id

    #return render_template("index1.html")
    return redirect("/noticias")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
@app.route("/divisas")
def divisas():
    return render_template("divisa.html")
