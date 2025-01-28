from flask import Flask, url_for, redirect, render_template, request, session
import mysql.connector
import numpy as np
import pickle

app = Flask(__name__)

host = "localhost"
user = "root"
password = ""
port = "3306"
database = "db"


mydb = mysql.connector.connect(host=host, user=user, password=password, port=port, database=database)
mycursor = mydb.cursor()


def executionquery1(query,values):
    mycursor.execute(query,values)
    mydb.commit()
    return

def retrivequery1(query,values):
    mycursor.execute(query,values)
    data = mycursor.fetchall()
    return data

def retrivequery2(query):
    mycursor.execute(query)
    data = mycursor.fetchall()
    return data


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    global user_id

    if request.method == "POST":
        name = request.form['username']
        email = request.form['useremail']
        age = request.form['age']
        age = int(age)
        gender = request.form['gender']
        print(222, gender)
        password = request.form['password']
        c_password = request.form['c_password']

        if password == c_password:
            query = "SELECT email FROM users"
            email_data = retrivequery2(query)

            email_data_list = []
            for i in email_data:
                email_data_list.append(i[0])

            if email.upper() not in email_data_list:
                query = "INSERT INTO users (name, email, password, age, gender) VALUES (%s, %s, %s, %s, %s)"
                values = (name.upper(), email.upper(), password.upper(), age, gender)
                executionquery1(query, values)

                query = "SELECT id FROM users ORDER BY id DESC LIMIT 1"
                user_id = retrivequery2(query)

                age_groups = {
                    "Age_Group_18_25": age >= 18 and age <= 25,
                    "Age_Group_26_35": age >= 26 and age <= 35,
                    "Age_Group_36_45": age >= 36 and age <= 45,
                    "Age_Group_46_55": age >= 46 and age <= 55,
                    "Age_Group_56_65": age >= 56 and age <= 65
                }

                gender_groups = {
                    "Gender_Female": gender.lower() == "female",
                    "Gender_Male": gender.lower() == "male"
                }

                values = tuple(age_groups.values()) + tuple(gender_groups.values())
                query = "INSERT INTO users_data (age_group_18_25, age_group_26_35, age_group_36_45, age_group_46_55, age_group_56_65, gender_female, gender_male) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                executionquery1(query, values)

                return render_template('login.html', message = 'Register Successfully!')
            return render_template('register.html', message="This email ID is already exists!")
        return render_template('register.html', message="Conform password is not match!")
    return render_template('register.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    global user_id
    if request.method == "POST":
        email = request.form['useremail']
        password = request.form['password']
        
        if email.upper() == "ADMIN@GMAIL.COM":
            if password == "admin":
                user_email = "ADMIN@GMAIL.COM"
                return render_template('admin_home.html')
            return render_template('login.html', message= "Invalid Password!!")
        
        query = "SELECT email FROM users"
        email_data = retrivequery2(query)

        email_data_list = []
        for i in email_data:
            email_data_list.append(i[0])

        if email.upper() in email_data_list:
            query = "SELECT id, password FROM users WHERE email = %s"
            values = (email.upper(),)
            password__data = retrivequery1(query, values)

            if password.upper() == password__data[0][1]:
                user_id = password__data[0][0]

                query = "UPDATE users_data SET login = login + 1 WHERE user_id = %s"
                values = (user_id,)
                executionquery1(query, values)

                return render_template('user_home.html')
            
            return render_template('login.html', message= "Invalid Password!!")
        return render_template('login.html', message= "This email ID does not exist!")
    return render_template('login.html')


@app.route("/user_home", methods=['GET', 'POST'])
def user_home():
    message = None
    if request.method == "POST":

        id = request.form['id']

        query = "SELECT * FROM cart WHERE product_id = %s AND user_id = %s"
        values = (id, user_id)
        data = retrivequery1(query, values)
        print(data)
        message = "This item already being in cart!"

        if not(data):
            query = "INSERT INTO cart (product_id, user_id) VALUES (%s, %s)"
            values = (id, user_id)
            executionquery1(query, values)

            query = "UPDATE users_data SET add_to_cart = add_to_cart + 1 WHERE user_id = %s"
            values = (user_id,)
            executionquery1(query, values)
            message = "Successfully added to cart!"

    query = "SELECT * FROM products"
    products = retrivequery2(query)
    return render_template("user_home.html", products = products ,active_page='home', message = message)


@app.route("/cart", methods=['GET', 'POST'])
def cart():
    message = None
    if request.method == "POST":
        product_id = request.form['product_id']
        quantity = request.form['quantity']
        amount = request.form['amount']

        query = "INSERT INTO purchases (product_id, quantity, amount, user_id) VALUES (%s, %s, %s, %s)"
        values = (product_id, quantity, amount, user_id)
        executionquery1(query, values)

        query = "UPDATE users_data SET avg_transaction_amount = avg_transaction_amount + %s, purchase = purchase + 1 WHERE user_id = %s"
        values = (amount, user_id)
        executionquery1(query, values)
        message = "Successfully Purchased!"
    
    query = "SELECT product_id FROM cart WHERE user_id = %s"
    values = (user_id,)
    cart_data = retrivequery1(query, values)
    products = []
    if cart_data:
        for i in cart_data:
            query = "SELECT * FROM products WHERE id = %s"
            values = (i[0],)
            data = retrivequery1(query, values)
            products.append(data)
    
    return render_template("cart.html", products=products, active_page='cart', message=message)


@app.route("/remove_cart", methods=["POST"])
def remove_cart():
    
    id = request.form['id']
    query = "DELETE FROM cart WHERE product_id = %s"
    values = (id,)
    executionquery1(query, values)
    return redirect("/cart")


@app.route("/admin_home", methods = ["GET", "POST"])
def admin_home():
    message = None
    user_id = None  # Define user_id with a default value
    if request.method == "POST":
        user_id = request.form['user_id']
        print(user_id)
        query = "SELECT * FROM users_data WHERE user_id = %s"
        values = (user_id,)
        data = retrivequery1(query, values)
        data_without_user_id = data[0][1:]
        print(data)
        print(data_without_user_id)
        reshaped_data = np.array(data_without_user_id).reshape(1, -1)

        with open('random_forest.pkl', 'rb') as f:
            loaded_model = pickle.load(f)

        classes=["Non fraudulent", "Fraudulent"]
        prediction = loaded_model.predict(reshaped_data)
        print(prediction)
        a = classes[prediction[0]]
        
        print(a)
        message = a
        print(message)

    query = "SELECT * FROM users_data"
    data = retrivequery2(query)
    return render_template("admin_home.html", datas=data, message=message, user_id=user_id)



'''
def admin_home():
    message = None
    if request.method == "POST":
        user_id = request.form['user_id']
        print(user_id)
        query = "SELECT * FROM users_data WHERE user_id = %s"
        values = (user_id,)
        data = retrivequery1(query, values)
        data_without_user_id = data[0][1:]
        print(data)
        print(data_without_user_id)
        reshaped_data = np.array(data_without_user_id).reshape(1, -1)

        with open('random_forest.pkl', 'rb') as f:
            loaded_model = pickle.load(f)
 
       
        model_dtype = [('left_child', '<i8'), ('right_child', '<i8'), ('feature', '<i8'), 
               ('threshold', '<f8'), ('impurity', '<f8'), ('n_node_samples', '<i8'), 
               ('weighted_n_node_samples', '<f8'), ('missing_go_to_left', 'u1')]

        structured_array = np.array(list(loaded_model.values()), dtype=model_dtype)
        model = structured_array

        classes=["Non fraudulent", "Fraudulent"]
        prediction = loaded_model.predict(reshaped_data)
        print(prediction)
        a = classes[prediction[0]]
        
        print(a)
        message = a
        print(message)

    query = "SELECT * FROM users_data"
    data = retrivequery2(query)
    return render_template("admin_home.html", datas = data, message = message, user_id = user_id)
'''
@app.route('/update_database', methods=['POST'])
def update_database():
    query = "UPDATE users_data SET browse = browse + 1 WHERE user_id = %s"
    values = (user_id,)
    executionquery1(query, values)
    return
















@app.route("/logout")
def logout():
    return redirect("/")

if __name__ == '__main__':
    app.run(debug = True)