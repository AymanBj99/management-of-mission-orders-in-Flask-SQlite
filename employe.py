from flask import Flask, request, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from modele import User, Mission
from db import db

app = Flask(__name__)