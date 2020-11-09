from rpgmanager.service import *
from rpgmanager.service import _generate_unique_room_code
from sqlalchemy import exc

class TestRPGManagerService:
    def test_create_campaign(self, mocker):
        # mocker comes from the pytest-mock package, includes mock, magicmock, patch, etc
        mock_session = mocker.MagicMock()
        mock_campaign = mocker.MagicMock(return_value=True)
        mock_code = mocker.MagicMock(return_value='abcd')
        mocker.patch('rpgmanager.service._generate_unique_room_code', mock_code)
        mocker.patch('rpgmanager.service.RPGManagerCampaign', mock_campaign)
        campaign = create_campaign(mock_session)
        assert campaign

    def test_create_campaign_error(self, mocker):
        mock_session = mocker.MagicMock()
        mock_code = mocker.MagicMock(return_value='abcd')
        mock_error = mocker.MagicMock(side_effect=exc.SQLAlchemyError)
        mocker.patch('rpgmanager.service._generate_unique_room_code', mock_code)
        mocker.patch('rpgmanager.service.RPGManagerCampaign', mock_error)
        campaign = create_campaign(mock_session)
        assert campaign is None

    def test_get_campaign_by_room_code(self, mocker):
        mock_session = mocker.MagicMock()
        mock_session.query().filter().one_or_none.return_value = mocker.MagicMock()
        campaign = get_campaign_by_room_code(mock_session, 'code')
        assert campaign.last_read_time is not None

    def test_get_campaign_by_room_code_error(self, mocker):
        mock_session = mocker.MagicMock()
        mock_session.query().filter().one_or_none.side_effect = exc.SQLAlchemyError
        assert get_campaign_by_room_code(mock_session, 'code') is None

    def test_update_campaign(self, mocker):
        mock_session = mocker.MagicMock()
        mock_campaign = mocker.MagicMock()
        mocker.patch('rpgmanager.service.get_campaign_by_room_code', mock_campaign)
        campaign = update_campaign(mock_session, 'code', name='name', region='region', day=9, party_level=1,
                                   money_ratio=10, notes='')
        assert campaign.day == 9

    def test_update_campaign_error(self, mocker):
        mock_session = mocker.MagicMock()
        mock_error = mocker.MagicMock(side_effect=exc.SQLAlchemyError)
        mocker.patch('rpgmanager.service.get_campaign_by_room_code', mock_error)
        assert update_campaign(mock_session, 'code') is None

    def test_create_player_6_players(self, mocker):
        mock_session = mocker.MagicMock()
        mock_campaign = mocker.MagicMock()
        mock_campaign.players = [1, 2, 3, 4, 5, 6]
        mock_get_campaign = mocker.MagicMock(return_value=mock_campaign)
        mocker.patch('rpgmanager.service.get_campaign_by_room_code', mock_get_campaign)
        assert not create_player(mock_session, 'code')

    def test_create_player(self, mocker):
        mock_session = mocker.MagicMock()
        mock_campaign = mocker.MagicMock()
        mock_campaign.players = [1, 2, 3]
        mock_get_campaign = mocker.MagicMock(return_value=mock_campaign)
        mocker.patch('rpgmanager.service.get_campaign_by_room_code', mock_get_campaign)
        mocker.patch('rpgmanager.service.RPGManagerCharacter')
        campaign = create_player(mock_session, 'code')
        assert len(campaign.players) == 3

    def test_create_player_error(self, mocker):
        mock_session = mocker.MagicMock()
        mock_error = mocker.MagicMock(side_effect=exc.SQLAlchemyError)
        mocker.patch('rpgmanager.service.get_campaign_by_room_code', mock_error)
        assert create_player(mock_session, 'code') is None

    def test_get_player_by_id(self, mocker):
        mock_session = mocker.MagicMock()
        mock_session.query().filter().one_or_none.return_value = True
        player = get_player_by_id(mock_session, 1)
        assert player

    def test_get_player_by_id_error(self, mocker):
        mock_session = mocker.MagicMock()
        mock_session.query().filter().one_or_none.side_effect = exc.SQLAlchemyError
        assert get_player_by_id(mock_session, 1) is None

    def test_update_character(self, mocker):
        mock_session = mocker.MagicMock()
        mock_character = mocker.MagicMock()
        mock_get_player = mocker.MagicMock(return_value=mock_character)
        mocker.patch('rpgmanager.service.get_player_by_id', mock_get_player)
        mocker.patch('rpgmanager.service.calc_player_money')
        update_character(mock_session, 'code', 1, name='alec', role='warrior', items='items',
                         notes='notes')
        assert mock_character.name == 'alec'

    def test_update_character_error(self, mocker):
        mock_session = mocker.MagicMock()
        mock_error = mocker.MagicMock(side_effect=exc.SQLAlchemyError)
        mocker.patch('rpgmanager.service.get_player_by_id', mock_error)
        update_character(mock_session, 'code')

    def test_calc_player_money_add_is_none(self, mocker):
        mock_session = mocker.MagicMock()
        mock_character = mocker.MagicMock()
        mock_character.campaign.money_ratio = 10
        calc_player_money(mock_character, gold=5, silver=0, copper=0, add=None)
        assert mock_character.money == 500

    def test_calc_player_money_add_is_false(self, mocker):
        mock_session = mocker.MagicMock()
        mock_character = mocker.MagicMock()
        mock_character.campaign.money_ratio = 10
        calc_player_money(mock_character, gold=5, silver=0, copper=0, dGold=1, add=False)
        assert mock_character.money == 400

    def test_delete_character(self, mocker):
        mock_session = mocker.MagicMock()
        mock_character = mocker.MagicMock()
        mock_character.campaign.room_code = 'code'
        mock_get_player = mocker.MagicMock(return_value=mock_character)
        mocker.patch('rpgmanager.service.get_player_by_id', mock_get_player)
        assert delete_character(mock_session, 'code', 1)

    def test_delete_character_not_found(self, mocker):
        mock_session = mocker.MagicMock()
        mocker.patch('rpgmanager.service.get_player_by_id')
        assert not delete_character(mock_session, 'code', 1)

    def test_delete_character_error(self, mocker):
        mock_session = mocker.MagicMock()
        mock_error = mocker.MagicMock(side_effect=exc.SQLAlchemyError)
        mocker.patch('rpgmanager.service.get_player_by_id', mock_error)
        assert not delete_character(mock_session, 'code', 1)

    def test_generate_unique_room_code(self, mocker):
        mock_session = mocker.MagicMock()
        mock_session.query().filter().one_or_none.return_value = False
        mock_code = mocker.MagicMock(return_value='code')
        mocker.patch('rpgmanager.service.generate_random_string', mock_code)
        code = _generate_unique_room_code(mock_session)
        assert code == 'code'

