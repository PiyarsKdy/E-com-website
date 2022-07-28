from flask import Flask, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import false, true
import json

local_server = true
with open('templates\config.json','r') as c:
    params = json.load(c)["params"]
app = Flask(__name__)
app.secret_key = 'cairocoders-ednalan'

if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
app.config['SQLALCHEMY_TRACK_MOIFICATIONS'] = false
db= SQLAlchemy(app)

class Users(db.Model):
    uname=db.Column(db.String(50),nullable=false,primary_key=true)
    email=db.Column(db.String(50),nullable=false)
    password=db.Column(db.String(50),nullable=false)

    def __init__(self,uname,email,password):
        self.uname=uname
        self.email=email
        self.password=password
    

class Checkout(db.Model):
    f_name=db.Column(db.String(50),nullable=false)
    l_name=db.Column(db.String(50),nullable=false)
    username=db.Column(db.String(80),primary_key=true,nullable=false)
    country=db.Column(db.String(50),nullable=false)
    state=db.Column(db.String(50),nullable=false)
    postcode=db.Column(db.Integer,nullable=false)
    address=db.Column(db.Text,nullable=false)


class Products(db.Model):
    slug=db.Column(db.String(100),nullable=false)
    cat_pro=db.Column(db.String(100),nullable=false)
    brand=db.Column(db.String(100),nullable=false)
    title=db.Column(db.String(100),nullable=false)
    price=db.Column(db.Float(precision=2),nullable=false)
    details=db.Column(db.String(1500),nullable=false)
    qty=db.Column(db.Integer,nullable=false)
    ram=db.Column(db.Integer,nullable=false)
    rom=db.Column(db.Integer,nullable=false)
    mrp=db.Column(db.Float(precision=2),nullable=false)
    offer=db.Column(db.Integer,nullable=true)
    pid=db.Column(db.BigInteger,nullable=false,primary_key=true)
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/shop")
def shop():
    prods = Products.query.filter_by().all()[0:9]
    return render_template('shop.html', prods=prods)

@app.route("/account", methods=['GET','POST'])
def account():
    if request.method == 'POST':
        uname=request.form.get('uname')
        email=request.form.get('email')
        password=request.form.get('password')

        userRes= Users.query.filter_by(uname=uname).first()
        if not uname or not email or not password:
            flash('fillout all the details.')
        elif userRes :
            flash('This username is already used.')
        else:
            user = Users(uname,email,password)
            db.session.add(user)
            db.session.commit()
            flash('You have successfully registered.')
        
    return render_template('account.html')
@app.route("/account/login", methods=['GET','POST'])
def login():
    if request.method=='POST':
        luname=request.form.get('luname')
        lpass=request.form.get('lpass')
        user = Users.query.filter_by(uname=luname).first()
        if (lpass == user.password):
            session['user']=luname
            return render_template('index.html')
    return render_template('account.html')
@app.route("/cart")
def cart():
    return render_template('cart.html')

@app.route("/checkout",methods=['GET','POST'])
def checkout():
    if(request.method=='POST'):
        print(request.form.get('state') )
        fname=request.form.get('fname')
        lname=request.form.get('lname')
        username=request.form.get('username')
        country=request.form.get('country')
        state=request.form.get('state')
        postcode=request.form.get('postcode')
        address=request.form.get('address')
        entry = Checkout(f_name=fname,l_name=lname,username=username,country=country,state=state,postcode=postcode, address=address)
        db.session.add(entry)
        db.session.commit()
    return render_template('checkout.html')

@app.route("/prod-details/<string:slug>", methods= ['GET'])
def prod_details_route(slug):
    prod = Products.query.filter_by(slug=slug).first()
    return render_template('prod-details.html', prod=prod)

@app.route("/wishlist")
def wishlist():
    return render_template('wishlist.html')


if __name__ == "__main__":
    app.run(debug=True)