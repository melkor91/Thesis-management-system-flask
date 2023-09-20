from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from config import config

# Controller:
from controllers.ControllerUser import ControllerUser
from controllers.ControllerAuthor import ControllerAuthor
#from controllers.ControllerTesis import ControllerTesis
#from controllers.ControllerCritico import ControllerCritico
#from controllers.ControllerRevision import ControllerRevision
#from controllers.ControllerAsesor import ControllerAsesor

# Entities:
from models.User import User
from models.Author import Author

app = Flask(__name__)

csrf = CSRFProtect()
app.url_map.strict_slashes = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3306/thesis_management'
db = SQLAlchemy(app)

login_manager_app=LoginManager(app)

@login_manager_app.user_loader
def load_user(user_id):
    return ControllerUser.get_by_id(db, user_id)

@app.route('/')
@app.route('/index')
@login_required
def home():
    #return redirect(url_for('login'))
    return render_template("home.html")

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return render_template("404.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'], 0)
        logged_user=ControllerUser.login(db,user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash ('Contraseña Inválida...', 'error')
                return render_template("auth/login.html")
        else:
            flash('Usuario No Encontrado...', 'error')
            return render_template("auth/login.html")
    else:
        return render_template("auth/login.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/register")
def register():
    return render_template("auth/register.html")

@app.route("/registerUser")
def registerUser():
    #Logic
    return redirect(url_for('login'))

@app.route('/usuarios')
@login_required
def usuarios():
    # Handle the usuarios page logic here
    return render_template('usuarios.html')

@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')

@app.route('/temas')
@login_required
def temas():
    # Handle the temas page logic here
    return render_template('temas.html')

@app.route('/libreria')
@login_required
def libreria():
    # Handle the librery page logic here
    return render_template('libreria.html')

# START TESIS ROUTES
@app.route('/tesis')
@login_required
def tesis():
    # Handle the library page logic here
    return render_template('components/tesis/index.html')

# START AUTOR ROUTES
@app.route('/autor')
@login_required
def autor():
    data = ControllerAuthor.getAutors(db)
    return render_template('components/autor/index.html', autores = data)

@app.route('/search_autores', methods=['POST'])
@login_required
def search():
    #try:
        name = request.form['keyname']
        data = ControllerAuthor.getAutorsbyName(db, name)
        return render_template('components/autor/resultado.html', filtered_autores=data)
    #except Exception as ex:
    #    print(ex)
    #    return redirect(url_for('autor'))    

@app.route('/create_autor_form', methods=['GET'])
@login_required
def create_autor_form():   
    return render_template('components/autor/create.html')

@app.route('/save_autor', methods=['POST'])
@login_required
def save_autor():
    try:
        student_code = request.form['student_code']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone = request.form['phone']
        address = request.form['address']
        email = request.form['email']
        ControllerAuthor.createAutor(db, student_code, firstname, lastname, phone, address, email)
        flash ("Autor Creado Exitosamente...")
        return redirect(url_for('autor'))
    except Exception as ex:
        return redirect(url_for('create_autor_form'))    

@app.route('/edit_autor_form/<int:id>', methods=['GET'])
@login_required
def edit_autor_form(id):
    autor = ControllerAuthor.get_autor_by_id(db, id)
    return render_template('components/autor/edit.html', autor=autor)

@app.route('/update_autor/<int:id>', methods=['POST'])
@login_required
def update_autor(id):
    try:
        student_code = request.form['student_code']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone = request.form['phone']
        address = request.form['address']
        email = request.form['email']
        ControllerAuthor.update_autor(db, id, student_code, firstname, lastname, phone, address, email)
        flash ("Autor Actualizado Exitosamente...")
        return redirect(url_for('autor'))
    except Exception as ex:
        flash ("No se pudo editar el Autor...")
        return redirect(url_for('edit_autor_form'))

@app.route('/desactivate_autor/<int:id>')
@login_required
def desactivate_autor(id):
    try:
        autor = ControllerAuthor.get_autor_by_id(db, id)
        if autor:
            # Set the is_deleted flag to 1
            ControllerAuthor.desactivate_autor(db, id)
            flash ("Autor Eliminado Exitosamente...")
            return redirect(url_for('autor'))
        else:
            flash ("No se pudo eliminar el Autor...")
            return redirect(url_for('autor'))
    except Exception as ex:
        raise Exception(ex)
           
# START ASESOR ROUTES
@app.route('/asesor')
@login_required
def asesor():
    # Handle the Authors page logic here
    return render_template('components/asesor/index.html')

@app.route('/review')
@login_required
def review():
    # Handle the Authors page logic here
    return render_template('components/review/index.html')

@app.route('/reviewer')
@login_required
def reviewer():
    # Handle the Authors page logic here
    return render_template('components/reviewer/index.html')
# END ROUTES COMPONENTS

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401,status_401)
    app.register_error_handler(404,status_404)
    app.run()


