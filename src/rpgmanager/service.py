from flask import request
from util import session_scope, loggingFactory
from sqlalchemy import exc
from model.db import RPGManagerCampaign, RPGManagerCharacter
from util.id_generator import generate_random_string
from datetime import datetime

_getLogger = loggingFactory('rpgmanager.service')


"""
Handles CRUD operations for the rpgmanager as well as some other misc functions.

create_campign
get_campaign_by_room_code
update_campaign

create_player
update_player
delete_player
"""


def create_campaign(session):
    """
    Creates a new campaign and returns the object to the user.
    """
    room_code = _generate_unique_room_code(session)
    try:
        new_campaign = RPGManagerCampaign(room_code=room_code,
                                        created_time=datetime.utcnow(),
                                        last_read_time=datetime.utcnow())
        session.add(new_campaign)
        session.commit()
        return new_campaign
    except exc.SQLAlchemyError as e:
        # log e
        return


def get_campaign_by_room_code(session, room_code):
    """
    Query and return a campaign that matches the given room code.

    :param session: The current session
    :param room_code: String, room code to ID the campaign
    :return: Campaign row
    """
    try:
        campaign = session.query(RPGManagerCampaign) \
                    .filter(RPGManagerCampaign.room_code==room_code) \
                    .one_or_none()
        # Update last read time
        campaign.last_read_time = datetime.utcnow()
        session.merge(campaign)
        session.commit()
        return campaign
    except (exc.SQLAlchemyError, AttributeError) as e:
        # log e
        return


def update_campaign(session, room_code, name=None, region=None,
                    day=None, party_level=None, money_ratio=None,
                    notes=None, **kwargs):
    """
    Update the campaign that matches the room_code with any provided values.
    """
    try:
        campaign = get_campaign_by_room_code(session, room_code)
        
        # Name and region could be an empty string
        if not name is None:
            campaign.name = name
        if not region is None:
            campaign.region = region
        if day:
            campaign.day = day
        if party_level:
            campaign.party_level = party_level
        if money_ratio:
            campaign.money_ratio = money_ratio
        if not notes is None:
            campaign.notes = notes

        campaign.last_updated_time = datetime.utcnow()

        session.merge(campaign)
        session.commit()
        return campaign
    except exc.SQLAlchemyError as e:
        # log e
        return


def create_player(session, room_code):
    """
    Create a player and add them to the campaign that matches the
    given room code.

    :param session: The current session
    :param room_code: String, room code to ID the campaign
    :return: Character row
    """
    try:
        campaign = get_campaign_by_room_code(session, room_code)
        # make sure there are not six or more players
        if len(campaign.players) >= 6:
            return False
        
        # otherwise, create and add the character to the campaign
        character = RPGManagerCharacter(campaign=campaign)
        session.add(character)
        session.commit()
        return campaign
    except exc.SQLAlchemyError as e:
        # log e
        return

def get_player_by_id(session, id):
    try:
        player = session.query(RPGManagerCharacter) \
                        .filter(RPGManagerCharacter.id==id) \
                        .one_or_none()
        return player
    except (exc.SQLAlchemyError, AttributeError) as e:
        # log e
        return

def update_character(session, room_code, id=None, name=None,
                     role=None, items=None, notes=None, **kwargs):
    """
    Update a character with given values.

    Class and money need to be handled specially since they have logic involved.

    :return: None
    """
    try:
        player = get_player_by_id(session, id)

        # calc player money and update player.money
        calc_player_money(player, **kwargs)

        if not name is None:
            player.name = name
        if role:
            player.role = role
        if not items is None:
            player.items = items
        if not notes is None:
            player.notes = notes
        session.merge(player)
        session.commit()
    except exc.SQLAlchemyError as e:
        # log e
        pass

def calc_player_money(player, gold=0, silver=0, copper=0, add=None,
                      dGold=0, dSilver=0, dCopper=0, **kwargs):
    """
    Calculate change to or set player money. Use the campaign's money_ratio for either
    base 10 or base 100 variations.

    Depending on variation, silver and copper should be less than the ratio, but shouldn't
    matter either way.

    value = gold * ratio^2 + silver * ratio + copper
    change = delta_gold * ratio^2 + delta_silver * ratio + delta_copper
    final value is value +/- change based on plus or minus (add var)
    
    Player cannot have negative money, so min is 0.

    If add is None, ignore any change and just update with gold, silver, and copper
    """
    ratio = player.campaign.money_ratio

    # Make sure all values are int
    gold = gold or 0
    silver = silver or 0
    copper = copper or 0
    dGold = dGold or 0
    dSilver = dSilver or 0
    dCopper = dCopper or 0

    current_value = int(gold) * ratio * ratio + int(silver) * ratio + int(copper)
    change_value = int(dGold) * ratio * ratio + int(dSilver) * ratio + int(dCopper)

    if add is None:
        new_value = max(current_value, 0)
    else:
        new_value = current_value + change_value if add else current_value - change_value
        new_value = max(new_value, 0)  # Minimum allowed money value is 0

    player.money = new_value


def delete_character(session, room_code, id):
    """
    Delete a character with the given id.

    Verify that the character and room_code match up.

    :return: Campaign
    """
    try:
        player = get_player_by_id(session, id)
        if player and player.campaign.room_code == room_code:
            session.delete(player)
            session.commit()
            return True
        else:
            return False
    except exc.SQLAlchemyError as e:
        # log e
        return False


def _generate_unique_room_code(session):
    """
    Attempts to generate a unique room code.
    Will try up to 5 times if a new code clashes with an existing one.

    :param session: The current session
    :return: String, the unique room code
    """
    for i in range(5):
        # Generate a code
        code = generate_random_string()

        # Check if it is currently being used
        campaign = session.query(RPGManagerCampaign).filter(RPGManagerCampaign.room_code==code).one_or_none()
        if not campaign:
            return code
    
