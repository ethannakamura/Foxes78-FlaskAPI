from flask import Blueprint, jsonify, request
from app.models import Player, db
from .apihelpers import token_required

# actually set up our blueprint and enable communication between our blueprint and the main flask app
# computers are dumb - if we don't tell the blueprint to exist, it won't exist
# and if we don't tell the application how to talk to the blueprint, it will have no idea how to talk to the blueprint
# instantiate a blueprint
api = Blueprint('api', __name__, url_prefix='/api')


# the decorator for a route belonging to a blueprint starts with @<blueprint_name> instead of @app
@api.route('/')
def test():
    return {'datadatadata': 'ooh look at this fancy data'}

@api.route('/players', methods=['GET'])
def players():
    """
    [GET] returns json data on all of the players in our database
    """
    players = [player.to_dict() for player in Player.query.all()]
    return jsonify(players)

@api.route('/player/<int:num>', methods=['GET'])
def get_number(num):
    '''
    [GET] /api/player/<int:num>
    returns all players with that number
    or None if no playes have that number
    '''
    players = Player.query.filter_by(number=num).all()
    if not players:
        return jsonify({num: None})
    return jsonify([x.to_dict() for x in players])

@api.route('/<string:tm>', methods=['GET'])
def get_team(tm):
    """
    [GET] /api/Manchester_City
    returns all players on the applicable team
    """
    tm = tm.replace('_', ' ') # team name from url will have an _ in place of the space -> replace that underscore with a space
    players = Player.query.filter_by(team=tm).all()
    if not players:
        return jsonify({tm: None})
    return jsonify([x.to_dict() for x in players])


# as we move into Create/Update/Delete routes - we need to accept information from the user
    # in order to actually perform the proper operations

# most popular case (for now) - when users submit POST requests (aka sending info to the API)
    # they're providing that info in the form of JSON data

@api.route('/createplayer', methods=['POST'])
@token_required
def createplayer():
    """
    [POST] /api/createplayer
    Accepts JSON data for the creation of a player in the following format:
    {
        'number': <int>,
        'first_name': <str>,
        'last_name': <str> optional default null,
        'position': <str>,
        'team': <str> optional default 'Free Transfer',
        'nationality': <str>,
        'transfer_cost': <str> optional default '$0m'
    }
    Checks if a player of the same name and number exists in the database
    Create the player in our database with a UUID
    Return a dictionary representation of that player in our database
    """
    data = request.get_json() # grabs the JSON data sent in the API POST request
    print(data)
    # fill in the last_name if not present
    if not data.get('last_name'):
        data['last_name'] = ''
    # check if a player of the same name and number exists already
        # query my database either by first_name, or last_name, or number
        # then check the data first_name, last_name, and number against my query results
    checks = Player.query.filter_by(last_name=data['last_name']).all()
    if checks:
        for p in checks:
            if p.first_name == data['first_name'] and p.number == data['number']:
                return jsonify({'Create Player Rejected': 'Player already exists.'})
    # create a player object and save to the database
    newplayer = Player()
    newplayer.from_dict(data)
    db.session.add(newplayer)
    db.session.commit()
    return jsonify({'Created': newplayer.to_dict()})


# update route - that lets someone update a player's information
@api.route('/update/<string:id>', methods=['PUT']) # PUT is used for updating existing things - just like POST, PUT can accept input
@token_required
def updateplayer(id):
    """
    [PUT] /api/update/<str:id>
    Accept a dictionary of all player attributes you wish to change - all key/value pairs are optional
    This route will work for changing every piece of a player's information or just one piece of a player's information
    {
        'number': <int>,
        'first_name': <str>,
        'last_name': <str>,
        'position': <str>,
        'team': <str>,
        'nationality': <str>,
        'transfer_cost': <str>
    }
    """
    data = request.get_json() # grabs the JSON data sent in the API PUT request
    print(data)
    # when it comes to updating the player information -> we already made a method to do this - we probably just have to change it a little
    # get the player object for this player id
    player = Player.query.get(id)
    if not player:
        return jsonify({'Update failed': 'No player with that ID'})
    player.from_dict(data)
    print(player.to_dict())
    db.session.commit()
    return jsonify({'Updated': player.to_dict()})

# delete route - that lets someone delete a player
@api.route('/delete/<string:id>', methods=['DELETE'])
@token_required
def deleteplayer(id):
    # check if a player of that id exists in the database
    p = Player.query.get(id)
    if not p: # if they don't exist, tell the user
        return jsonify({'Delete failed':'No player of that ID exists in the database'})
    # implied else that player does exist
    db.session.delete(p)
    db.session.commit()
    return jsonify({'Deleted':p.to_dict()})