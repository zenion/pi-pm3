
import config

from flask import Flask, request, render_template, jsonify
import pexpect
import re

app = Flask(__name__)

pm3 = pexpect.spawn('proxmark3 ' + config.proxmark3_device)
pm3.expect('ARM7TDMI')


def read_lf_card():
    pm3.sendline('lf search')
    i = pm3.expect(['No Known Tags Found!', 'Valid HID Prox ID Found!'])
    if i == 0:
        output = 'Could not find a card, try again.'
    elif i == 1:
        re_search_output = re.search('HID Prox TAG ID: (.+?) - Format', pm3.before)
        output = 'Card Found: ' + re_search_output.group(1)
    else:
        output = 'error!'
    return output


def read_hf_card():
    pass


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/read')
def read():
    reader_output = read_lf_card()
    return jsonify(result=reader_output)

if __name__ == "__main__":
    app.run(
            host='0.0.0.0',
            port=5000,
            )
