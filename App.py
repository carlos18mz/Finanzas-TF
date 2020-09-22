import datetime
import math
import decimal
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, g, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# pip install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy mysqlclient
# pip install mysqlclient
# pip install pipenv gunicorn
# pip freeze > requirements.txt
# touch Procfile 
# inside gunicorn print => web: gunicorn App:app
# git push heroku master
# heroku config:set DATABASE_URL='mysql://uv1d04zrxpnefepn:qm6Qum3mzDQZgKLCiCLc@b9gqzffgxhbnvmbdttw0-mysql.services.clever-cloud.com:3306/b9gqzffgxhbnvmbdttw0'



# MYSQL CONNECTION
#app.config['MYSQL_HOST']='b9gqzffgxhbnvmbdttw0-mysql.services.clever-cloud.com'
#app.config['MYSQL_PASSWORD']='qm6Qum3mzDQZgKLCiCLc'
#app.config['MYSQL_USER']='uv1d04zrxpnefepn'
#app.config['MYSQL_DB']='b9gqzffgxhbnvmbdttw0'


# LOCALHOST

#app.config['MYSQL_HOST']='localhost'
#app.config['MYSQL_PASSWORD']=''
#app.config['MYSQL_USER']='root'
#app.config['MYSQL_DB']='finanzas'

#mysql = MySQL(app)

#SQLALCHEMY
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://uv1d04zrxpnefepn:qm6Qum3mzDQZgKLCiCLc@b9gqzffgxhbnvmbdttw0-mysql.services.clever-cloud.com:3306/b9gqzffgxhbnvmbdttw0"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

#LOCALHOST
#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost:3306/finanzas"
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)
#ma = Marshmallow(app)

#==========================================================================
#========= ENTITYS =======================================================>
#==========================================================================

class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column("id", db.Integer, primary_key=True)
    email = db.Column("email" ,db.String(50), unique=True)
    password = db.Column("password", db.String(50),unique=False, nullable=False)
    firstName = db.Column("first_name", db.String(50), nullable=False)
    lastName = db.Column("last_name",db.String(50), nullable=False)
    dni = db.Column("dni",db.String(50), nullable=False)
    phone = db.Column("phone",db.String(50), nullable=False)
    creditLine = db.relationship('CreditLine' , backref='customers',
                                lazy='dynamic')

    def __init__(self, email, password, firstName, lastName, dni, phone):
        self.email = email
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.dni = dni
        self.phone = phone
        self.phone = phone
    
    def __repr__(self):
        return f"Customer('{self.id}', '{self.email}', '{self.password}', '{self.firstName}', '{self.lastName}', '{self.dni}', '{self.phone}')"

class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column("id", db.Integer, primary_key=True)
    email = db.Column("email" ,db.String(50), unique=True)
    password = db.Column("password", db.String(50),unique=False, nullable=False)
    firstName = db.Column("first_name", db.String(50), nullable=False)
    lastName = db.Column("last_name",db.String(50), nullable=False)
    dni = db.Column("dni",db.String(50), nullable=False)
    phone = db.Column("phone",db.String(50), nullable=False)
    creditLine = db.relationship('CreditLine', backref='admins',
                                lazy='dynamic')

    def __init__(self, email, password, firstName, lastName, dni, phone):
        self.email = email
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.dni = dni
        self.phone = phone
    
    def __repr__(self):
        return f"Admin('{self.id}', '{self.email}', '{self.password}', '{self.firstName}', '{self.lastName}', '{self.dni}', '{self.phone}')"

class CreditLine(db.Model):
    __tablename__ = "credit_lines"
    
    id = db.Column("id", db.Integer, primary_key=True)
    adminId = db.Column("admin_id", db.Integer, db.ForeignKey('admins.id'))
    customerId = db.Column("customer_id", db.Integer, db.ForeignKey('customers.id'))
    initialDate = db.Column("initial_date", db.DateTime, nullable=False)
    finishDate = db.Column("finish_date" , db.DateTime, nullable=False)
    interestRate = db.Column("interest_rate", db.Float(), nullable=False)
    totalAmountLended = db.Column("total_amount_lended", db.Float(), nullable=False)
    totalAmountPay = db.Column("total_amount_pay", db.Float(), nullable=False)
    remainingAmount = db.Column("remaining_amount", db.Float(), nullable=False)
    paydays = db.Column("paydays", db.Integer, nullable=False)
    eachPayment = db.Column("each_payment", db.Float(), nullable=False)    
    feeDone = db.Column("fee_done", db.Integer, nullable=False)
    transactions = db.relationship('Transaction', backref="credit_lines", 
                                lazy='dynamic')

    def __init__(self, adminId, customerId, initialDate, finishDate, interestRate, totalAmountLended, paydays, feeDone):
        self.adminId = adminId
        self.customerId = customerId
        self.initialDate = initialDate
        self.finishDate = finishDate
        self.interestRate = interestRate
        self.totalAmountLended = totalAmountLended
        self.totalAmountPay = float(self.totalAmountLended) + float(self.totalAmountLended * float(self.interestRate/100))
        self.remainingAmount = self.totalAmountPay
        self.paydays = paydays
        ep = float(self.totalAmountPay/self.paydays); ep += 0.01
        self.eachPayment = "%.2f" % round(ep, 2)
        self.feeDone = feeDone

    def __repr__(self):
        return f"CreditLine('{self.id}','{self.adminId}','{self.initialDate}','{self.finishDate}','{self.interestRate}', '{self.totalAmountLended}', '{self.totalAmountPay}','{self.remainingAmount}','{self.transactions}', '{self.paydays}', '{self.eachPayment}', '{self.feeDone}')"

class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column("id", db.Integer, primary_key=True)
    creditLineId = db.Column("credit_line_id", db.Integer, db.ForeignKey("credit_lines.id"))
    amount = db.Column("amount", db.Float(), nullable=False)
    transactionDate = db.Column("transaction_date", db.DateTime, nullable=False)
    feeNumber = db.Column("fee_number",db.Integer, nullable=False)

    def __init__(self, creditLineId, amount, transactionDate, feeNumber):
        self.creditLineId = creditLineId
        self.amount = amount
        self.transactionDate = transactionDate
        self.feeNumber = feeNumber

    def __repr__(self):
        return f"Transaction('{self.id}', '{self.creditLineId}', '{self.amount}', '{self.transactionDate}', '{self.feeNumber}')"


db.create_all()
#=============================================================================================
#====================== ROUTES ===============================================================>
#=============================================================================================

# SETTINGS
app.secret_key = 'uv1d04zrxpnefepn:qm6Qum3mzDQZgKLCiCLc@b9gqzffgxhbnvmbdttw0-b9gqzffgxhbnvmbdttw0'

#LOAD USER ACCOUNT
@app.before_request
def before_request():
    if 'user_id' in session:
        user = db.session.query(Customer).filter_by(id = session['user_id']).all()
        g.user = user

@app.route('/')
def index():
    return render_template("landingPage.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('user_id', None)
    emailf = request.form['email']
    passwordf = request.form['password']
    customer = db.session.query(Customer).filter_by(email = emailf, password = passwordf).all()

    if customer:
        session['user_id'] = customer[0].id
        before_request()
        print("customer id : ", customer[0].id)        
        return redirect(url_for("dashboard"))
    else:
        flash('Credenciales incorrectas')
        return render_template("signIn.html")

@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for("index"))

@app.route('/loanApplication', methods=['GET','POST'])
def loanApplication():
    totalMount = request.form['totalMount']
    months  = request.form["month"]
    initialDate = request.form['fecha']
    rrr = request.form;
    print("totalmount : ", totalMount)
    print("tcea : ",months)
    print("all : ", rrr)

    customer = db.session.query(Customer).filter_by(id = session['user_id']).first()
    admin = db.session.query(Admin).filter_by(id = 1).first()

    print("Customer : ", customer)
    print("Admin : ", admin)

    print("totalMount type : ",type(totalMount))
    print("Months type : ",type(months))
    new_credit_line = CreditLine(admin.id, customer.id, initialDate, initialDate, float(30), float(totalMount), int(months), 0)
    db.session.add(new_credit_line)
    db.session.commit()
    return redirect(url_for("dashboard"))

@app.route('/cancelLoanApplication', methods=['GET', 'POST'])
def cancelLoanApplication():
    return redirect(url_for("dashboard"))

@app.route('/pay-credit-fee/<id>', methods=['GET', 'POST'])
def payCreditFee(id):
    creditLine = db.session.query(CreditLine).filter_by(id = id).first()
    creditLine.feeDone = creditLine.feeDone + 1
    currentMountPay = float(creditLine.remainingAmount)
    reachPay = float(creditLine.eachPayment)
    creditLine.remainingAmount = float(currentMountPay - reachPay)
    db.session.commit()
    newTransaction = Transaction(creditLine.id, reachPay, datetime.datetime.now(), creditLine.id)
    db.session.add(newTransaction)
    db.session.commit()
    return redirect(url_for("dashboard"))


#Routes
@app.route("/sign-in", methods=['GET','POST'])
def signin():
    return render_template("signIn.html")

@app.route("/sign-up", methods=['GET','POST'])
def signup():
    return render_template("signUp.html")

@app.route("/new-user", methods=['POST'])
def newUser():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        dni = request.form['dni']
        phone = request.form['phone']

        new_customer =  Customer(email,password,firstName,lastName, dni, phone)
        db.session.add(new_customer)
        db.session.commit()
        flash('Usuario registrado satisfactoriamente, ingresa sesión para comenzar a usar la aplicación')
        return redirect(url_for("signin"))

@app.route('/dashboard')
def dashboard():
    creditLines =  db.session.query(CreditLine).filter_by(customerId = session['user_id']).all()
    print("creditLines : ",creditLines)
    creditLinesId =  db.session.query(CreditLine.id).filter_by(customerId = session['user_id']).all()
    print("creditLinesId : ",creditLinesId)
    result_dict = [a for b in creditLinesId for a in b]
    print("creditlInesId result dict : ",result_dict)
    transactions = db.session.query(Transaction).filter_by(creditLineId = Transaction.creditLineId.in_(result_dict)).all()
    return render_template("dashboard.html", creditLines = creditLines, transactions = transactions)

@app.route('/new-credit-line', methods=['GET','POST'])
def new_credit_line():
    return render_template("newCreditLine.html")

@app.route('/add_contact', methods=['POST'])
def add_contact():
    return None


@app.route('/edit/<id>')
def get_contact(id):
    return None

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        return None

@app.route('/delete/<string:id>')
def delete_contact(id):
    return None


if __name__ == '__main__':
    app.run(port = 3000, debug = True) 
