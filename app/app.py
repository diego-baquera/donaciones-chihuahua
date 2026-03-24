# Se importa la clase flask de la propia libreria de flask, 
# es la clase encargada de levantar la aplicacion, el servidor no funciona sin este importe.
from flask import Flask, render_template, redirect, url_for, request
from flask_mysqldb import MySQL

# Creacion de la instancia de aplicación, _name_ es una varible estatica especial de python
# le dice a flask donde esta ubicado el archivo principal y donde buscar recursos. Nunca cambia.
app = Flask(__name__)

# Conexion a MYSQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'donaciones'

conexion = MySQL(app)

# Decoradores de ruta, sirven para que flask sepa que funciones
# ejecutar cuando alguien entre en alguna ruta en especifico
@app.route("/")
# Funcion normal de python, lo que sea que esta funcion haga es lo que vera el usuario en el navegador
def index():
    # return '<h1 style="color: blue;">Hola Carlos, tu servidor Flask está funcionando.<h1>'
    categorias = [
        "Todas",
        "Donaciones Económicas",
        "Ropa",
        "Alimentos y Despensas",
        "Juguetes",
        "Materiales de Construcción",
        "Otros"
    ]
    
    data = {
        'titulo': 'Despensas Bienestar',
        'bienvenida': 'Bienvenido a Despensas Bienestar',
        'numero_botones': len(categorias),
        'botones': categorias
        }

    # Si existe un parametro llamado categoria en la url lo captura en categoria y lo imprime en la terminal
    categoria = request.args.get("categoria")

    try:
        cursor = conexion.connection.cursor()


        if categoria and categoria != "Todas":

            sql = """
            SELECT 
            centros.id_centro,
            centros.nombre,
            centros.descripcion,
            centros.direccion,
            centros.telefono,
            centros.email,
            centros.pagina_web,
            categorias.nombre
            FROM centros
            JOIN centro_categoria 
            ON centros.id_centro = centro_categoria.id_centro
            JOIN categorias 
            ON categorias.id_categoria = centro_categoria.id_categoria
            WHERE categorias.nombre = %s
            """

            cursor.execute(sql, (categoria,))

        else:

            sql = """
            SELECT 
            centros.id_centro,
            centros.nombre,
            centros.descripcion,
            centros.direccion,
            centros.telefono,
            centros.email,
            centros.pagina_web,
            GROUP_CONCAT(categorias.nombre SEPARATOR ', ') AS categorias
            FROM centros
            JOIN centro_categoria 
            ON centros.id_centro = centro_categoria.id_centro
            JOIN categorias 
            ON categorias.id_categoria = centro_categoria.id_categoria
            GROUP BY centros.id_centro
            """
            cursor.execute(sql)
        centros = cursor.fetchall()
        print(centros)

        cursor.close()

    except Exception as ex:
        print("ERROR SQL:", ex)
        data['mensaje'] = 'Error'
        centros = []

    # 4) Mandar centros al HTML
    return render_template("index.html", data=data, centros=centros)

def pagina_no_encontrada(error):
    return render_template('404.html'), 404

    # redirect redirige al usuario a otra URL
    # url_for genera la URL de una ruta usando el nombre de la función de Flask
    #return redirect(url_for('index'))


@app.route("/about")
def about():
    return "Página sobre nosotros"

@app.route("/contacto")
def contacto():
    return "Contactanos"
    
if __name__ == "__main__":
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True)