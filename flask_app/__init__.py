from flask import Flask, render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = '3262197dfc1612902661a492d99a04ff6c91e51bc19cc46f32ecb7f9b39df994'