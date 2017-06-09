#!/usr/bin/python
#coding:utf-8
from Tkinter import *
from ttk import *
from fractions import gcd
import sys
import random
import time
import string


def euclid(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = euclid(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = euclid(a, m)
    return x % m


def squ_mul(x, exponents):
    exponentsList = [int(m) for m in list('{0:0b}'.format(exponents))]
    exponentsList.reverse()
    del exponentsList[0]
    y = x
    for exp in exponentsList:
        y = pow(y, 2)
        if (exp == 1):
            y = y * x
    return y

def getPrime(n, testcase=5):
    assert n >= 2
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    s = 0
    d = n - 1
    while True:
        quotient, remainder = divmod(d, 2)
        if remainder == 1:
            break
        s = s + 1
        d = quotient
    assert (2**s * d == n - 1)

    def composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2**i * d, n) == n - 1:
                return False
        return True

    for i in range(testcase):
        a = random.randrange(2, n)
        if composite(a):
            return False
    return True


def rsa(plaintext, keylength):
    messsage = plaintext
    q_len = keylength / 2
    p_len = q_len - 2
    p = 2
    q = 2
    left = squ_mul(2, p_len - 1)
    right = squ_mul(2, p_len)
    left_q_len = squ_mul(2, q_len - 1)
    right_q_len = squ_mul(2, q_len)
    is_prime = True
    while is_prime:
        rand = random.randint(left, right)
        if getPrime(rand):
            is_prime = False
            p = rand
    is_prime = True
    while is_prime:
        rand = random.randint(left_q_len, right_q_len)
        if getPrime(rand):
            is_prime = False
            q = rand
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 0
    i = 2
    while (i < phi):
        step = random.randint(2, keylength)
        if gcd(i, phi) == 1:
            e = i
            break
        i = i + step
    d = modinv(e, phi)
    plain = messsage
    cipher = pow(plain, e, n)
    return p, q, n, e, d, plain, cipher


def rsa_dec(d, p, q, cipher):
    dp = d % (p - 1)
    dq = d % (q - 1)
    qp = modinv(q, p) % p
    m1 = pow(cipher % p, dp, p)
    m2 = pow(cipher % q, dq, q)
    h = (qp * (m1 - m2)) % p
    decrypted = m2 + h * q
    return decrypted


class GUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.text_plain = Entry(self)
        self.text_plain["width"] = 10
        self.text_plain.grid(column=0, row=0)

        self.label_one = Label(self)
        self.label_one["text"] = "plaintext"
        self.label_one.grid(column=0, row=1)

        self.text_enc = Entry(self)
        self.text_enc["width"] = 10
        self.text_enc.grid(column=1, row=0)

        self.label_two = Label(self)
        self.label_two["text"] = "ciphertext"
        self.label_two.grid(column=1, row=1)

        self.text_dec = Entry(self)
        self.text_dec["width"] = 10
        self.text_dec.grid(column=2, row=0)

        self.label_three = Label(self)
        self.label_three["text"] = "decrypted"
        self.label_three.grid(column=2, row=1)

        self.encrypt = Button(self)
        self.encrypt["text"] = "Encryption"
        self.encrypt.grid(column=1, row=3)
        self.encrypt["command"] = self.encrypt_button

        self.decrypt = Button(self)
        self.decrypt["text"] = "Decryption"
        self.decrypt.grid(column=2, row=3)
        self.decrypt["command"] = self.decrypt_button

    def encrypt_button(self):
        self.plaintext = self.text_plain.get()
        keylength = 1024
        p, q, n, e, d, plain, cipher = rsa(int(self.plaintext), keylength)
        self.d = d
        self.p = p
        self.q = q
        self.text_enc.delete(0, END)
        self.text_enc.insert(0, cipher)

    def decrypt_button(self):
        self.cipher = self.text_enc.get()
        decrypted = rsa_dec(
            int(self.d), int(self.p), int(self.q), int(self.cipher))
        self.text_dec.delete(0, END)
        self.text_dec.insert(0, decrypted)


if __name__ == '__main__':
    win = Tk()
    win.title("hw3")
    win = GUI(master=win)
    win.mainloop()
