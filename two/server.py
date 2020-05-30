from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///development.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100))

    def __repr__(self):
        return '<Student %r>' % self.id

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        student_name = request.form['name']
        student_surname = request.form['surname']
        new_student = Student(name=student_name, surname=student_surname)

        try:
            db.session.add(new_student)
            db.session.commit()
            return redirect("/")
        except:
            return "No se pudo guardar el estudiante"
    else:
        students = Student.query.order_by(Student.id).all()
        return render_template("index.html", students=students)

@app.route("/editar/<int:id>", methods=['POST', 'GET'])
def editar(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.surname = request.form['surname']
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "No se pudo actualizar "
    else:
        return render_template("editar.html", student=student)

@app.route("/eliminar/<int:id>")
def eliminar(id):
    student_delete = Student.query.get_or_404(id)
    try:
        db.session.delete(student_delete)
        db.session.commit()
        return redirect("/")
    except:
        "No se pudo eliminar el estudiante"

if __name__ == "__main__":
    start_db = sys.argv[1] if len(sys.argv) > 1 else ""
    db.create_all() if start_db == "start_db" else None
    print("===== Database Created =====") if start_db == "start_db" else None

    app.run(debug=True)
