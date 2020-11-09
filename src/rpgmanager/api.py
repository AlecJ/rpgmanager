from flask import request, jsonify
from util import session_scope, loggingFactory
from svc import app
from rpgmanager.service import (create_campaign, get_campaign_by_room_code, update_campaign, 
                                create_player, update_character, delete_character)

_getLogger = loggingFactory('rpgmanager.api')

"""
Routes and methods:

POST /rpgmanager/campaign
    rpgmanager_create_campaign:
    Client creates a new Campaign. A campaign is returned and the user
    is redirected to their page.

GET /rpgmanager/campaign
    rpgmanager_get_campaign:
    Client attempts to get a campaign.

PUT /rpgmanager/campaign
    rpgmanager_update_campaign:
    Handles updating campaign info and all characters in a campaign.

POST /rpgmanager/character
    rpgmanager_create_character:
    Creates and adds a character to a given campaign via room code.

PUT /rpgmanager/character
    rpgmanager_update_money:
    Handles calculator function of adding and subtracting money for a
    given player.

DELETE /rpgmanager/character
    rpgmanager_delete_character:
    Deletes a character by id but verifies room code.
"""


@app.route("/rpgmanager/campaign", methods=["POST"])
def rpgmanager_create_campaign():
    """
    Client creates a new Campaign. A campaign is returned and the user
    is redirected to their page.
    """
    logger = _getLogger('rpgmanager_create_campaign')
    
    with session_scope() as session:
        campaign = create_campaign(session)
        if campaign:
            logger.info('create campaign: {}'.format(campaign.room_code))
            return campaign.row_as_dict(), 200
        else:
            logger.error("Error creating new room.")
            return "Error creating a new room.", 400

@app.route("/rpgmanager/campaign", methods=["GET"])
def rpgmanager_get_campaign():
    """
    Client attempts to get a campaign.
    """
    with session_scope() as session:
        # make sure the room code is valid
        room_code = request.args.get('campaignId')
        if not room_code:
            return "Invalid room code provided: {}".format(room_code), 400
        
        campaign = get_campaign_by_room_code(session, room_code)
        if campaign:
            return campaign.row_as_dict(), 200
        else:
            return "Room with code {} does not exist.".format(room_code), 400

@app.route("/rpgmanager/campaign", methods=["PUT"])
def rpgmanager_update_campaign():
    """
    Handles updating campaign info and all characters in a campaign.
    """
    with session_scope() as session:
        data = request.json.get('data')
        # make sure the room code is valid
        room_code = request.json.get('campaignId')
        if not room_code:
            return "Invalid room code provided: {}".format(room_code), 400
        
        # update players
        for character in data.get('characters', []):
            update_character(session, room_code, **character)
        campaign = update_campaign(session, room_code, **data)
        if campaign:
            return campaign.row_as_dict(), 200
        else:
            return "Room with code {} does not exist.".format(room_code), 400

@app.route("/rpgmanager/character", methods=["POST"])
def rpgmanager_create_character():
    """
    Creates and adds a character to a given campaign via room code.
    """
    with session_scope() as session:
        # make sure the room code is valid
        room_code = request.json.get('campaignId')
        if not room_code:
            return "Invalid room code provided: {}".format(room_code), 400
        
        campaign = create_player(session, room_code)
        if campaign:
            return campaign.row_as_dict(), 200
        else:
            return "There are already six characters in the campaign.", 400

@app.route("/rpgmanager/character", methods=["PUT"])
def rpgmanager_update_money():
    """
    Handles calculator function of adding and subtracting
    money for a given player.
    """
    with session_scope() as session:
        # make sure the room code is valid
        room_code = request.json.get('campaignId')
        if not room_code:
            return "Invalid room code provided: {}".format(room_code), 400
        
        character = request.json.get('data')
        update_character(session, room_code, **character)

        try:
            campaign = get_campaign_by_room_code(session, room_code)
            if campaign:
                return campaign.row_as_dict(), 200
            else:
                return "Room with code {} does not exist.".format(room_code), 400
        except Exception as e:
            # log error
            return "Error processing request", 400


@app.route("/rpgmanager/character", methods=["DELETE"])
def rpgmanager_delete_character():
    """
    Deletes a character by id but verifies room code.
    """
    with session_scope() as session:
        # make sure the room code is valid
        room_code = request.json.get('campaignId')
        character_id = request.json.get('characterId')
        if not room_code:
            return "Invalid room code provided: {}".format(room_code), 400

        if delete_character(session, room_code, character_id):
            campaign = get_campaign_by_room_code(session, room_code)
            if campaign:
                return campaign.row_as_dict(), 200
        
        return "Could not delete character.", 400
