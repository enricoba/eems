# -*- coding: utf-8 -*-
"""
Initiation module for eems.
"""

# import external modules
import os
import math
import numpy
import time
import datetime
from threading import Thread, Lock
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.sql import func


# import eems modules
from sensors import ds18b20


class _SensorDictionary(object):
    def __init__(self, s_list):
        tmp = dict()
        for s in s_list:
            tmp[s] = None
        self.dic = tmp
        self.lock = Lock()

    def set_temp(self, sensor, temp):
        with self.lock:
            self.dic[sensor] = temp

    def get_dic(self):
        return self.dic

    def reset_dic(self):
        for sensor in self.dic.keys():
            self.dic[sensor] = None


"""
eems project information
"""


__project__ = 'eems'
__version__ = '0.2.0.1b1'
__copyright__ = '2015-2016, Henrik Baran, Aurofree Hoehn'
__author__ = 'Henrik Baran, Aurofree Hoehn'


# Flask object
app = Flask(__name__)

# check if server or development environment
if os.path.exists('/var/www/eems/eems/data/'):
    path = '/var/www/eems/eems/data/config.db'
else:
    path = '{}/data/config.db'.format(os.path.dirname(os.path.realpath(__file__)))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////{}'.format(path)
db = SQLAlchemy(app)


class General(db.Model):
    __tablename__ = 'general'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    item = db.Column(db.Text)
    value = db.Column(db.Text)

    def __init__(self, item=None, value=None):
        self.item = item
        self.value = value


class Content(db.Model):
    __tablename__ = 'content'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    position = db.Column(db.Text)
    german = db.Column(db.Text)
    english = db.Column(db.Text)

    def __init__(self, position=None, german=None, english=None):
        self.position = position
        self.german = german
        self.english = english


class Sessions(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    session = db.Column(db.Text)
    interval = db.Column(db.Integer)
    end_time = db.Column(db.Integer)
    monitoring = db.Column(db.Integer)

    def __init__(self, session=None, interval=None, end_time=None, monitoring=0):
        self.session = session
        self.interval = interval
        self.end_time = end_time
        self.monitoring = monitoring


class SensorsUsed(db.Model):
    __tablename__ = 'sensors_used'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    code = db.Column(db.Text)
    name = db.Column(db.Text)
    value = db.Column(db.REAL)
    session_id = db.Column(db.Integer)
    sensor_id = db.Column(db.Integer)

    def __init__(self, code=None, name=None, value=None, session_id=None, sensor_id=None):
        self.code = code
        self.name = name
        self.value = value
        self.session_id = session_id
        self.sensor_id = sensor_id


class SensorsSupported(db.Model):
    __tablename__ = 'sensors_supported'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.Text)
    typ = db.Column(db.Text)
    unit = db.Column(db.Text)

    def __init__(self, name=None, typ=None, unit=None):
        self.name = name
        self.typ = typ
        self.unit = unit


class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    timestamp = db.Column(db.Integer)
    value = db.Column(db.Float)
    sensor_name_id = db.Column(db.Integer)

    def __init__(self, timestamp=None, value=None, sensor_name_id=None):
        self.timestamp = timestamp
        self.value = value
        self.sensor_name_id = sensor_name_id


w_flag = 1


def w_monitor(interval):
    global w_flag

    s_ds18b20 = ds18b20.DS18B20()

    query = General.query.filter_by(item='SESSION').first()
    s_tmp = Sessions.query.filter_by(session=query.value).first()
    session_id = s_tmp.id
    query = SensorsSupported.query.filter_by(name='ds18b20').first()
    sensor_id = query.id
    tmp_sensors = SensorsUsed.query.filter_by(session_id=session_id, sensor_id=sensor_id).all()

    s_list = list()
    s_names_ids = dict()
    for i in tmp_sensors:
        s_list.append(i.code)
        s_names_ids[i.code] = i.id
    s_dict = _SensorDictionary(s_list)

    timestamp = int(time.time() / interval) * interval
    timestamp += interval
    time.sleep(timestamp - time.time())
    while w_flag == 1:
        time_now = int(time.time())
        threads = list()
        for s in s_list:
            threads.append(Thread(target=s_ds18b20.read, args=(s, s_dict)))
        for t in threads:
            t.setDaemon(True)
            t.start()
        for t in threads:
            t.join()
        for code in s_list:
            tmp = Data(timestamp=time_now, value=s_dict.dic[code], sensor_name_id=s_names_ids[code])
            db.session.add(tmp)
        db.session.commit()

        timestamp += interval
        time.sleep(timestamp - time.time())


def w_watchdog(end_time, interval):
    global w_flag
    timestamp = int(time.time() / interval) * interval
    timestamp += interval
    duration = end_time - time.time()
    time.sleep(duration - 1)
    w_flag = 0


def __db_content(lang):
    tmp_dict = dict()
    content = Content.query.all()
    for i in content:
        if lang == 'de':
            tmp_dict[i.position] = i.german
        elif lang == 'en':
            tmp_dict[i.position] = i.english
    return tmp_dict


def __db_general():
    tmp_dict = dict()
    general = General.query.all()
    for i in general:
        tmp_dict[i.item] = i.value
    return tmp_dict


@app.route('/', methods=['GET', 'POST'])
def start():
    return redirect(url_for('index', lang='en'))


@app.route('/<string:lang>/', methods=['GET', 'POST'])
def index(lang=None):
    # level-0 :: CONTENT
    if lang is None:
        content = __db_content('en')
    else:
        language = General.query.filter_by(item='LANGUAGE').first()
        language.value = lang
        db.session.commit()
        content = __db_content(lang)

    profiles = [content['HOME_NEW'].encode('utf-8')]
    sessions = Sessions.query.all()
    for i in sessions:
        profiles.append(i.session.encode('utf-8'))

    if request.method == 'POST':
        if 'session-start' in request.form:
            # get new session input
            profile_tmp = request.form['session-input']

            # verify if new session (input text has a length) or existing session (length = 0)
            if len(profile_tmp):
                session = General.query.filter_by(item='SESSION').first()
                session.value = profile_tmp
                session_add = Sessions(profile_tmp)
                db.session.add(session_add)
            else:
                profile_load = request.form['session-load']
                session = General.query.filter_by(item='SESSION').first()
                session.value = profile_load

            # update session related information
            status = General.query.filter_by(item='NAVBAR_STATUS').first()
            icon = General.query.filter_by(item='SESSION_ICON').first()
            color = General.query.filter_by(item='SESSION_COLOR').first()
            status.value = ''
            icon.value = 'lock'
            color.value = 'green'
            db.session.commit()

            # get session id from sessions table by session name of general table
            query = General.query.filter_by(item='SESSION').first()
            s_id = Sessions.query.filter_by(session=query.value).first()

            # update session_id in general table
            session_id = General.query.filter_by(item='SESSION_ID').first()
            session_id.value = s_id.id
            db.session.commit()

            return redirect(url_for('config', lang=lang))
        elif 'sessionLogout' in request.form:
            session = General.query.filter_by(item='SESSION').first()
            status = General.query.filter_by(item='NAVBAR_STATUS').first()
            icon = General.query.filter_by(item='SESSION_ICON').first()
            color = General.query.filter_by(item='SESSION_COLOR').first()
            session_id = General.query.filter_by(item='SESSION_ID').first()
            session.value = '-'
            status.value = 'disabled'
            icon.value = 'unlock'
            color.value = 'darkred'
            session_id.value = '-'
            db.session.commit()

            # level-99 :: CONFIG
            global_data = __db_general()
            return render_template('index.html', name='index', version=__version__,
                                   global_data=global_data,
                                   content=content,
                                   profiles=profiles, len=len(profiles))
    else:
        # level-99 :: CONFIG
        global_data = __db_general()
        return render_template('index.html', name='index', version=__version__,
                               global_data=global_data,
                               content=content,
                               profiles=profiles, len=len(profiles))


@app.route('/update/', methods=['GET'])
def update():
    query = General.query.filter_by(item='SESSION').first()
    s_tmp = Sessions.query.filter_by(session=query.value).first()
    session_id = s_tmp.id
    for i in request.args.items():
        sensor = SensorsUsed.query.filter_by(code=i[0], session_id=session_id).first()
        sensor.name = i[1]
    db.session.commit()
    return jsonify()


@app.route('/config/', methods=['GET', 'POST'])
@app.route('/<string:lang>/config/', methods=['GET', 'POST'])
def config(lang=None):
    # level-0 :: CONTENT
    if lang is None:
        content = __db_content('en')
    else:
        language = General.query.filter_by(item='LANGUAGE').first()
        language.value = lang
        db.session.commit()
        content = __db_content(lang)

    # level-2 :: DB
    query = General.query.filter_by(item='SESSION').first()
    s_tmp = Sessions.query.filter_by(session=query.value).first()
    session_id = s_tmp.id

    # level-3 :: HANDLING
    if request.method == 'POST':
        if 'config-start' in request.form:
            interval = int(request.form['interval'])
            end_time = int(time.mktime(datetime.datetime.strptime(request.form['datetime'],
                                                                  '%d-%m-%Y %H:%M').timetuple()))
            s_tmp.interval = interval
            s_tmp.end_time = end_time
            s_tmp.monitoring = 1
            db.session.commit()

            # start monitoring
            t = Thread(target=w_monitor, args=(interval, ))
            w = Thread(target=w_watchdog, args=(end_time, interval, ))
            t.setDaemon(True)
            w.setDaemon(True)
            w.start()
            t.start()
        return redirect(url_for('monitor', lang=lang))
    else:
        # if data then read database else actual time and no value interval
        if s_tmp.interval is None:
            at = math.ceil((time.time() / 300)) * 300
            tmp = datetime.datetime.fromtimestamp(at)
            timedate = tmp.strftime('%d-%m-%Y %H:%M')
            interval = ''
            flag = 0
        else:
            tmp = datetime.datetime.fromtimestamp(s_tmp.end_time)
            timedate = tmp.strftime('%d-%m-%Y %H:%M')
            interval = s_tmp.interval
            flag = 1

        # level-10 :: SENSORS - DS18B20
        s_ds18b20 = ds18b20.DS18B20()
        s_list = s_ds18b20.detect()
        if len(s_list):
            query = SensorsSupported.query.filter_by(name='ds18b20').first()
            sensor_id = query.id
            s_dict = _SensorDictionary(s_list)
            threads = list()
            for s in s_list:
                threads.append(Thread(target=s_ds18b20.read, args=(s, s_dict)))
            for t in threads:
                t.setDaemon(True)
                t.start()
            for t in threads:
                t.join()
            for code in s_list:
                sensor = SensorsUsed.query.filter_by(code=code, session_id=session_id).first()
                if sensor is None:
                    tmp = SensorsUsed(code=code, value=s_dict.dic[code], session_id=session_id, sensor_id=sensor_id,
                                      name='')
                    db.session.add(tmp)
                else:
                    sensor.value = s_dict.dic[code]
            db.session.commit()

        # level-99 :: DB
        sensors_used = SensorsUsed.query.filter_by(session_id=session_id).all()
        sensors_supported = SensorsSupported.query.all()

        global_data = __db_general()
        return render_template('index.html', name='config', version=__version__,
                               global_data=global_data,
                               content=content, timedate=timedate, interval=interval, flag=flag,
                               sensors_used=sensors_used,
                               sensors_supported=sensors_supported)


@app.route('/monitor/')
@app.route('/<string:lang>/monitor/')
def monitor(lang=None):
    # level-0 :: CONTENT
    if lang is None:
        content = __db_content('en')
    else:
        language = General.query.filter_by(item='LANGUAGE').first()
        language.value = lang
        db.session.commit()
        content = __db_content(lang)

    # level-1 :: VALUES
    query = General.query.filter_by(item='SESSION').first()
    s_tmp = Sessions.query.filter_by(session=query.value).first()
    session_id = s_tmp.id

    sensors_used = SensorsUsed.query.filter_by(session_id=session_id).all()
    sensors_supported = SensorsSupported.query.all()

    # TESTS
    for row in db.session.query(SensorsUsed.code.label('code')).all():
        print row.code

    now = time.time()
    print 'start ', now
    """test = db.session.query(db.func.count(Data.value), Data.value, Data.sensor_name_id).\
        group_by(Data.value).\
        group_by(Data.sensor_name_id).\
        filter(Data.sensor_name_id < 20).\
        filter(Data.sensor_name_id > 1).all()"""
    maxi = db.session.query(db.func.max(Data.value)).scalar()
    print 'max: ', maxi

    sums = db.session.query(db.func.sum(Data.value).label('a1')).group_by(Data.id)
    print 'sums: ', sums
    # average = db.session.query(db.func.avg(sums.subquery().columns.a1)).scalar()
    average = db.session.query(db.func.avg(Data.value)).\
        filter(Data.sensor_name_id < 20).\
        scalar()
    print 'avg: ', average
    print 'mitte', time.time() - now
    """
    now = time.time()
    test_list = list()
    for i in test:
        print i
        test_list.append(i.value)
    print 'ende ', time.time() - now
    print len(test_list)"""

    # level-99 :: CONFIG
    global_data = __db_general()
    return render_template('index.html', name='monitor', version=__version__,
                           global_data=global_data,
                           content=content,
                           sensors_used=sensors_used, sensors_supported=sensors_supported)


@app.route('/licence/')
@app.route('/<string:lang>/licence/')
def licence(lang=None):
    # level-0 :: CONTENT
    if lang is None:
        content = __db_content('en')
    else:
        language = General.query.filter_by(item='LANGUAGE').first()
        language.value = lang
        db.session.commit()
        content = __db_content(lang)

    time_now = int(time.time())
    for x in range(100000):
        tmp = Data(timestamp=time_now, value=20, sensor_name_id=20)
        db.session.add(tmp)
    db.session.commit()

    # level-99 :: CONFIG
    global_data = __db_general()
    return render_template('index.html', name='licence', version=__version__,
                           global_data=global_data,
                           content=content)


if __name__ == "__main__":
    # in deployment MUST be False !!!
    app.debug = True
    app.run(host='0.0.0.0')
