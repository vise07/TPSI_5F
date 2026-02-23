import socket
import tkinter as tk
from tkinter import messagebox


def connetti_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 12345))
    return client


def ricevi_concerti(client):
    data = client.recv(1024).decode()
    lista = data.split(",")
    return lista


def acquista():
    