"""

Tests are written with pytest.

Run from root directory with

`pynt test` to run tests

or

`pynt coverage` to get a coverage report


Below is an excample using magicmock and patch

    mock_session = mocker.MagicMock()
    mock_campaign = mocker.MagicMock(return_value=True)
    mock_code = mocker.MagicMock(return_value='abcd')
    mocker.patch('rpgmanager.service._generate_unique_room_code', mock_code)
    mocker.patch('rpgmanager.service.RPGManagerCampaign', mock_campaign)
    campaign = create_campaign(mock_session)
    assert campaign


You can raise an error with...

    mock_error = mocker.MagicMock(side_effect=exc.SQLAlchemyError)
    mocker.patch('rpgmanager.service.RPGManagerCampaign', mock_error)

"""