#!/usr/bin/env python3
"""
Asset web service
"""

import requests
import json
from flask import Flask, request as flask_req, abort, jsonify
from bs4 import BeautifulSoup as bs

app = Flask(__name__)
CBR_BASE_URL = "https://www.cbr.ru/eng"
CBR_DAILY_URL = f"{CBR_BASE_URL}/currency_base/daily/"
CBR_KEY_INDICATORS_URL = f"{CBR_BASE_URL}/key-indicators/"


def parse_cbr_currency_base_daily(s: str) -> dict:
    """parse_cbr_currency_base_daily"""
    currency_rate = {}

    soup = bs(s, 'html.parser')
    html_c = soup.find('html')
    body_c = html_c.find('body')
    div_c_0 = body_c.find('div', id='content')

    div_c_1 = div_c_0.find('div', class_='offsetMenu')
    div_c_2 = div_c_1.find('div', class_='container-fluid')
    div_c_3 = div_c_2.find('div', class_='col-md-23 offset-md-1')
    div_c_4 = div_c_3.find('div', class_='table-wrapper')
    div_c_5 = div_c_4.find('div', class_='table')

    table_c = div_c_5.find('table', class_='data')
    table_body = table_c.find('tbody')

    rows = table_body.find_all('tr')
    for i in range(1, len(rows)):
        row = rows[i]
        tds = row.find_all('td')

        char_code = tds[1].string
        unit = float(tds[2].string.replace(",", ""))
        rate = float(tds[4].string.replace(",", ""))

        currency_rate[char_code] = rate / unit

    return currency_rate


def parse_cbr_key_indicators(s: str) -> dict:
    """parse_cbr_key_indicators"""
    currency_rate = {}

    soup = bs(s, 'html.parser')
    html_c = soup.find('html')
    body_c = html_c.find('body')
    div_c_0 = body_c.find('div', id='content')

    div_c_1 = div_c_0.find('div', class_='offsetMenu')
    div_c_2 = div_c_1.find('div', class_='container-fluid')
    div_c_3 = div_c_2.find('div', class_='col-md-23 offset-md-1')
    div_c_4 = div_c_3.find('div', class_='dropdown')
    div_c_5 = div_c_4.find('div', class_='dropdown_content')
    div_c_6 = div_c_5.find_all('div', class_='key-indicator_content offset-md-2')

    for k in range(2):
        div_c_7 = div_c_6[k].find('div', class_='key-indicator_table_wrapper')
        div_c_8 = div_c_7.find('div', class_='table key-indicator_table')
        table_c = div_c_8.find('table')
        table_body = table_c.find('tbody')

        rows = table_body.find_all('tr')

        for i in range(1, len(rows)):
            row = rows[i]
            tds = row.find_all('td')
            div_1 = tds[0].find('div')
            div_2 = div_1.find_all('div')
            char_code = div_2[1].string
            value_2 = float(tds[-1].string.replace(",", ""))

            currency_rate[char_code] = value_2

    return currency_rate


class AssetPortfolio:
    def __init__(self, name):
        self.name = name
        self.asset_dict = {}

    def cleanup(self):
        """cleanup"""
        self.asset_dict = {}

    def calculate_all_revenue(self, period: int) -> float:
        """calculate_revenue"""
        cbr_daily_response = requests.get(CBR_DAILY_URL)
        cbr_key_indicators_response = requests.get(CBR_KEY_INDICATORS_URL)
        if not (cbr_daily_response.ok or cbr_key_indicators_response.ok):
            raise ValueError()
        currency_dict = parse_cbr_currency_base_daily(cbr_daily_response.text)
        metal_dict = parse_cbr_key_indicators(cbr_key_indicators_response.text)

        total_revenue = 0
        for asset in self.asset_dict.values():
            if asset.char_code in metal_dict:
                rate = metal_dict[asset.char_code]
            else:
                rate = currency_dict.get(asset.char_code, 0)
            revenue = asset.calculate_revenue(period, rate)
            total_revenue += revenue

        return total_revenue

    def get_asset_list(self, name_list=None):
        asset_list = []
        for asset in self.asset_dict.values():
            if name_list is None or asset.name in name_list:
                asset_repr = [asset.char_code, asset.name, asset.capital, asset.interest]
                asset_list.append(asset_repr)
        asset_list = sorted(asset_list, key=lambda x: x[1])
        asset_list = sorted(asset_list, key=lambda x: x[0])
        return asset_list


class Asset:
    def __init__(self, char_code: str, name: str, capital: float, interest: float):
        self.char_code = char_code
        self.name = name
        self.capital = capital
        self.interest = interest

    def calculate_revenue(self, years: int, rate: float) -> float:
        """calculate_revenue"""
        revenue = rate * self.capital * ((1.0 + self.interest) ** years - 1.0)
        return revenue


@app.route("/cbr/daily")
def cbr_daily():
    """CBR daily handler"""
    try:
        cbr_daily_response = requests.get(CBR_DAILY_URL)
        if not cbr_daily_response.ok:
            abort(503)
        currency_dict = parse_cbr_currency_base_daily(cbr_daily_response.text)
        return currency_dict
    except:
        abort(503)


@app.route("/cbr/key_indicators")
def cbr_key_indicators():
    """CBR key indicators handler"""
    try:
        cbr_key_indicators_response = requests.get(CBR_KEY_INDICATORS_URL)
        if not cbr_key_indicators_response.ok:
            abort(503)
        metal_dict = parse_cbr_key_indicators(cbr_key_indicators_response.text)
        return metal_dict
    except:
        abort(503)


@app.route("/api/asset/add/<char_code>/<name>/<float:capital>/<float:interest>")
@app.route("/api/asset/add/<char_code>/<name>/<float:capital>/<int:interest>")
@app.route("/api/asset/add/<char_code>/<name>/<int:capital>/<float:interest>")
@app.route("/api/asset/add/<char_code>/<name>/<int:capital>/<int:interest>")
def add_asset(char_code, name, capital, interest):
    """Add asset handler"""
    if name not in asset_portfolio.asset_dict:
        new_asset = Asset(char_code, name, float(capital), float(interest))
        asset_portfolio.asset_dict[name] = new_asset
        return f"Asset '{name}' was successfully added", 200
    return f"Asset '{name}' is already exist", 403


@app.route("/api/asset/list")
def get_asset_list():
    """Get asset handler"""
    asset_list = asset_portfolio.get_asset_list()
    return jsonify(asset_list)


@app.route("/api/asset/get")
def get_some_asset_list():
    """Get asset handler"""
    user_name_list = flask_req.args.getlist("name")
    asset_list = asset_portfolio.get_asset_list(user_name_list)
    return jsonify(asset_list)


@app.route("/api/asset/cleanup")
def cleanup_portfolio():
    """Cleanup handler"""
    asset_portfolio.cleanup()
    return '', 200


@app.route("/api/asset/calculate_revenue")
def calculate_revenue():
    """calculate_revenue"""
    try:
        user_period = flask_req.args.getlist("period")
        revenues = {}
        for period in user_period:
            revenue = asset_portfolio.calculate_all_revenue(int(period))
            revenues[str(int(period))] = revenue
        return jsonify(revenues)
    except:
        abort(503)


@app.errorhandler(404)
def page_not_found(_error):
    """404 handler"""
    return "This route is not found", 404


@app.errorhandler(503)
def page_do_not_exist(_error):
    """503 handler"""
    return 'CBR service is unavailable', 503


asset_portfolio = AssetPortfolio("main_portfolio")
#app.run(debug=True)
