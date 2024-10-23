from flask import Flask, session, redirect, url_for, request, render_template

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para usar sesiones en Flask

# Función para generar un ID único
def generate_id():
    return max((p['id'] for p in session.get('products', [])), default=0) + 1

@app.route('/')
def index():
    if 'products' not in session:
        session['products'] = []
    return render_template('index.html', products=session['products'])

@app.route('/add', methods=['POST'])
def add_product():
    product = {
        'id': generate_id(),
        'nombre': request.form['nombre'],
        'cantidad': int(request.form['cantidad']),
        'precio': float(request.form['precio']),
        'fecha_vencimiento': request.form['fecha_vencimiento'],
        'categoria': request.form['categoria']
    }
    session['products'].append(product)
    session.modified = True  # Indicamos que la sesión ha sido modificada
    return redirect(url_for('index'))

@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    session['products'] = [p for p in session['products'] if p['id'] != product_id]
    session.modified = True  # Indicamos que la sesión ha sido modificada
    return redirect(url_for('index'))

@app.route('/edit/<int:product_id>', methods=['POST'])
def edit_product(product_id):
    for product in session['products']:
        if product['id'] == product_id:
            product['nombre'] = request.form['nombre']
            product['cantidad'] = int(request.form['cantidad'])
            product['precio'] = float(request.form['precio'])
            product['fecha_vencimiento'] = request.form['fecha_vencimiento']
            product['categoria'] = request.form['categoria']
    session.modified = True  # Indicamos que la sesión ha sido modificada
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
