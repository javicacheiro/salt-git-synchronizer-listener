from flask import jsonify, request
from . import api, db, app
from .models import State, Pillar
from datetime import datetime
import subprocess


@api.route('/saltenvs/states', methods=['GET'])
def get_states_saltenvs():
    results = State.query.all()
    states = []
    for state in results:
        states.append(state.name)
    return jsonify({'states': states})


@api.route('/saltenvs/states/<name>', methods=['GET'])
def get_state_saltenv(name):
    state = State.query.filter_by(name=name).first_or_404()
    return jsonify({'name': state.name,
                    'last_updated': state.last_updated})


@api.route('/saltenvs/states/<name>', methods=['PUT'])
def sync_state_saltenv(name):
    state = State.query.filter_by(name=name).first_or_404()
    state.last_updated = datetime.now()
    db.session.add(state)
    db.session.commit()
    subprocess.call(['sudo', '/usr/local/bin/git_sync_states', state.name])
    app.logger.info('Synchronizing /srv/salt/{0}'.format(state.name))
    app.logger.info('sudo /usr/local/bin/git_sync_states {0}'.format(state.name))
    return '', 204


@api.route('/saltenvs/states', methods=['POST'])
def add_new_state_saltenv_from_git_repo():
    data = request.get_json()
    name = data['name']
    state = State(name=name)
    db.session.add(state)
    db.session.commit()
    return '', 201


@api.route('/saltenvs/pillars', methods=['GET'])
def get_pillars_saltenvs():
    results = Pillar.query.all()
    pillars = []
    for pillar in results:
        pillars.append(pillar.name)
    return jsonify({'pillars': pillars})


@api.route('/saltenvs/pillars/<name>', methods=['GET'])
def get_pillar_saltenv(name):
    pillar = Pillar.query.filter_by(name=name).first_or_404()
    return jsonify({'name': pillar.name,
                    'last_updated': pillar.last_updated})


@api.route('/saltenvs/pillars/<name>', methods=['PUT'])
def sync_pillar_saltenv(name):
    pillar = Pillar.query.filter_by(name=name).first_or_404()
    pillar.last_updated = datetime.now()
    db.session.add(pillar)
    db.session.commit()
    subprocess.call(['sudo', '/usr/local/bin/git_sync_pillars', pillar.name])
    app.logger.info('Synchronizing /srv/pillar/{0}'.format(pillar.name))
    app.logger.info('sudo /usr/local/bin/git_sync_pillars {0}'.format(pillar.name))
    return '', 204


@api.route('/saltenvs/pillars', methods=['POST'])
def add_new_pillar_saltenv_from_git_repo():
    data = request.get_json()
    name = data['name']
    pillar = Pillar(name=name)
    db.session.add(pillar)
    db.session.commit()
    return '', 201


@api.route('/saltenvs/states/test', methods=['PUT'])
def echo_data():
    data = request.get_json()
    app.logger.info('data: {0}'.format(data))
    app.logger.warn('data: {0}'.format(data))
    app.logger.error('data: {0}'.format(data))
    return jsonify({'message': 'Hello'})


@api.route('/saltenvs/test', methods=['GET'])
def echo_hello():
    return jsonify({'message': 'Hello'})
