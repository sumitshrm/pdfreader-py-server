import camelot
import pandas as pd
from flask import Flask, jsonify, request, render_template, flash
file = "files/pnb.pdf"
tables = camelot.read_pdf(file, pages='1')
print("Total tables extracted:", tables.n)
tables.export('bar.json', f='json')


