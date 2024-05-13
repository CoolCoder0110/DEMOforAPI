from flask import Flask, render_template, request, redirect, url_for
import requests
import random  # Importerar viktiga moduler

app = Flask(__name__)  # init flask

API_BASE_URL = "http://localhost:5000/api"  # base url


@app.route('/')  # route index
def index():
    return render_template('index.html')


@app.route('/add_user', methods=['GET', 'POST'])  # route lägger till user
def add_user():
    if request.method == 'POST':  # hantera post
        name = request.form.get('name')
        email = request.form.get('email')
        if not name or not email:  # validera user input
            return render_template('error.html', message="Name and Email are required.")

        user_id = generate_user_id()  # genererat user id
        data = {'user_id': user_id, 'name': name, 'email': email}
        response = requests.post(f"{API_BASE_URL}/users", json=data)  # Post för att skapa user
        if response.status_code == 201:
            return redirect('/')
        else:
            return render_template('error.html', message="Failed to create user.")

    return render_template('add_user.html')


@app.route('/users')  # route för att visa alla users
def users():
    response = requests.get(f"{API_BASE_URL}/users")  # skickar get t api
    if response.status_code == 200:  # hanterar response
        users = response.json()
        return render_template('all_users.html', users=users)
    else:
        return render_template('error.html', message="Failed to retrieve users.")


@app.route('/user/<string:user_id>')  # Route för att visa user details
def user_details(user_id):
    response = requests.get(f"{API_BASE_URL}/users/{user_id}")  # get request t api
    if response.status_code == 200:  # hanterar response från api
        user = response.json()
        return render_template('user_details.html', user=user)
    else:
        return render_template('error.html', message="User not found.")


@app.route('/delete_user/<string:user_id>')  # route för radera användare
def delete_user(user_id):
    response = requests.delete(f"{API_BASE_URL}/users/{user_id}")  # skickar delete
    if response.status_code == 204:
        return redirect(url_for('users'))
    else:
        return render_template('error.html', message="Failed to delete user.")


@app.route('/add_movie/<string:user_id>', methods=['GET', 'POST'])  # route för att adda movie t user
def add_movie(user_id):
    if request.method == 'POST':  # hantera post req
        imdb_id = request.form.get('imdb_id')
        if not imdb_id:
            return render_template('error.html', message="IMDB ID is required.")

        data = {'user_id': user_id, 'imdb_id': imdb_id, 'action': 'add'}  # data för api request
        response = requests.put(f"{API_BASE_URL}/users/{user_id}", json=data)  # skicka post req
        if response.status_code == 200:
            return redirect(url_for('user_details', user_id=user_id))
        else:
            return render_template('error.html', message="Failed to add movie.")

    return render_template('add_movie.html', user_id=user_id)  # rendera template


@app.route('/remove_movie/<string:user_id>/<string:imdb_id>', methods=['POST'])  # route för att ta bort film från user
def remove_movie(user_id, imdb_id):
    data = {'user_id': user_id, 'imdb_id': imdb_id, 'action': 'remove'}  # hantera api req
    response = requests.put(f"{API_BASE_URL}/users/{user_id}", json=data)  # skicka put t api
    if response.status_code == 200:
        return redirect(url_for('user_details', user_id=user_id))
    else:
        return render_template('error.html', message="Failed to remove movie.")


def generate_user_id():
    return ''.join(random.choices('0123456789', k=4))  # funktion för att generera random user id


if __name__ == '__main__':  # starta flask
    app.run(debug=True, port=5050)
