from model import db
from util import config
from util import json_serializable
import math
import enum


class RPGManagerClass(enum.Enum):
    barbarian = "barbarian"
    bard = "bard"
    cleric = "cleric"
    druid = "druid"
    fighter = "fighter"
    monk = "monk"
    paladin = "paladin"
    ranger = "ranger"
    rogue = "rogue"
    sorcerer = "sorcerer"
    warlock = "warlock"
    wizard = "wizard"


class RPGManagerCampaign(db.Model):
    __tablename__ = 'rpg_manager_campaign'

    id = db.Column(db.Integer(), primary_key=True)
    room_code = db.Column(db.String(4), nullable=False, unique=True)

    players = db.relationship('RPGManagerCharacter', backref='campaign', order_by="RPGManagerCharacter.id.desc()")

    name = db.Column(db.String(100))
    region = db.Column(db.String(100))
    day = db.Column(db.Integer())
    party_level = db.Column(db.Integer())
    money_ratio = db.Column(db.Integer(), default=10)
    notes = db.Column(db.String(3000))
    created_time = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    last_read_time = db.Column(db.TIMESTAMP(timezone=True), nullable=False)

    def row_as_dict(self):
        return {
            "id": self.room_code,
            "name": self.name,
            "region": self.region,
            "day": self.day,
            "party_level": self.party_level,
            "money_ratio": self.money_ratio,
            "notes": self.notes,
            "characters": [player.row_as_dict() for player in self.players]
        }

    def __repr__(self):
        return "RPGManagerCampaign(id={}, room={}, name={})".format(self.id, self.room_code, self.name)



class RPGManagerCharacter(db.Model):
    __tablename__ = 'rpg_manager_character'

    id = db.Column(db.Integer(), primary_key=True)

    campaign_id = db.Column(db.ForeignKey(RPGManagerCampaign.id, ondelete="cascade"), index=True, nullable=False)

    name = db.Column(db.String(25), default="New Character")
    role = db.Column(db.Enum(RPGManagerClass))
    money = db.Column(db.Integer(), default=0)
    items = db.Column(db.String(1000))
    notes = db.Column(db.String(1000))

    def row_as_dict(self):
        gold, silver, copper = self.split_money()

        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "gold": gold,
            "silver": silver,
            "copper": copper,
            "items": self.items,
            "notes": self.notes
        }

    def split_money(self):
        """
        Currency is stored as an int but display as gold silver and copper.

        Depending on the money ratio of a campaign, silver and copper could
        go up to 10 or 100.
        """
        ratio = self.campaign.money_ratio
        gold, silver, copper = (0, 0, 0)
        value = self.money
        # Gold is either worth 100 or 10,000
        if value >= ratio * ratio:
            gold = math.floor(value / (ratio * ratio))
            value -= gold * ratio * ratio
        # Silver is either worth 10 or 100
        if value >= ratio:
            silver = math.floor(value / ratio)
            value -= silver * ratio
        # The rest must be copper
        copper = value
        return (gold, silver, copper)

    def __repr__(self):
        return "RPGManagerCharacter(id={}, room={}, name={})".format(self.id, self.campaign.room_code, self.name)
