
import config

from flask import Flask, request, render_template, jsonify
import pexpect
import re

app = Flask(__name__)

pm3 = pexpect.spawn('proxmark3 ' + config.proxmark3_device)
pm3.expect('proxmark3>')


def read_lf_card():
    pm3.sendline('lf search')
    i = pm3.expect(['No Known Tags Found!', 'Valid HID Prox ID Found!', 'Valid Indala ID Found!'])
    if i == 0:
        output = 'Could not find a card, try again.'
        card_hex = ''
        return output, card_hex
    elif i == 1:
        re_search_output = re.search('HID Prox TAG ID: (.+?) - Format', pm3.before)
        output = 'Card Found: ' + re_search_output.group(1)
        card_hex = re_search_output.group(1).split()[0]
        return output, card_hex
    else:
        output = 'ERROR! Consult your local Josh for more details.  ' + pm3.before
        card_hex = ''
        return output, card_hex

def write_lf_card(card_hex):
    pm3.sendline('lf hid clone ' + card_hex)
    pm3.expect('DONE!')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/read')
def read():
    reader_output_tuple = read_lf_card()
    reader_output_print, reader_output_hex = reader_output_tuple[0], reader_output_tuple[1]
    return jsonify(result=reader_output_print, card_hex=reader_output_hex)


@app.route('/write')
def write():
    card_uri_variable = 'id'
    if card_uri_variable in request.args:
        write_lf_card(request.args[card_uri_variable])
        return jsonify(card_hex=request.args[card_uri_variable], cloned=True, result="Clone Complete.")
    else:
        return 'Missing card_hex argument'

if __name__ == "__main__":
    app.run(
            host='0.0.0.0',
            port=5000,
            )
