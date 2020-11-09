import React, { Component } from 'react'
import { debounce } from 'throttle-debounce'
import RPGLobby from './RPGLobby'
import RPGManagerHeader from './RPGManagerHeader'
import Party from './Party'
import Notes from './Notes'
import Monsters from './Monsters'
import SlideInDiv from '../common/util/SlideInDiv'
import {
    create_campaign,
    get_campaign,
    update_campaign,
    create_character,
    delete_character,
    calc_money,
} from '../../api/rpg_api'

class RPGManagerView extends Component {
    constructor(props) {
        super(props)

        this.state = {
            gameId: !!this.props.match.params.id ? this.props.match.params.id : null,
            campaign: null,
            loadFailed: false,
            isSaving: false,
            stillSaving: false,
            showNotes: false,
            roomCode: !!this.props.match.params.id ? this.props.match.params.id : null,
        }

        // intermediate cache resolves changes made during round trip updating backend
        this.cacheState = {
            campaign: null
        }

        this.handleChange = this.handleChange.bind(this)
        this.toggleNotes = this.toggleNotes.bind(this)
        this.createCampaign = this.createCampaign.bind(this)
        this.createCharacter = this.createCharacter.bind(this)
        this.handleCharacterChange = this.handleCharacterChange.bind(this)
        this.calcMoney = this.calcMoney.bind(this)
        this.setOldDeltaCurrencyValuesForPlayer = this.setOldDeltaCurrencyValuesForPlayer.bind(this)
        this.deleteCharacter = this.deleteCharacter.bind(this)
    }

    handleChange(e) {
        const { name, type, value } = e.target

        let newValue = value
        if (type === 'checkbox') {
            // Note: This money ratio code is a mess, has had several `fixes`
            // its complexity lies in that it needs to trigger an update on
            // player money values, since we are changing between 
            // 10x and 100x copper = 1 silver, etc
            if (name === 'money_ratio') {
                newValue = this.state['campaign']['money_ratio'] === 10 ? 100 : 10
            } else {
                // checkbox, toggle
                newValue = !this.state[name]
            }
            

        }

        // handle gamestate changes
        if (
            name === 'name' ||
            name === 'region' ||
            name === 'day' ||
            name === 'party_level' ||
            name === 'money_ratio' ||
            name === 'notes'
        ) {
            const { campaign: oldCampaign } = this.state
            this.setState({ campaign: { ...oldCampaign, [name]: newValue } })
        }

        this.setState({ [name]: newValue, isSaving: true }, () => {
            if (name === 'money_ratio') {
                this.update_campaign_force()
            } else {
                this.debounce_update_campaign()
            }
        })
    }

    handleCharacterChange = (id) => (e) => {
        const { name, value } = e.target
        const { campaign: oldCampaign } = this.state

        // iterate through characters and replace with the updated values
        const characters = oldCampaign.characters.map((c) => {
            if (c.id === id) {
                return { ...c, [name]: value }
            } else {
                return c
            }
        })

        this.setState({ campaign: { ...oldCampaign, characters } })


        // don't update if delta values
        if (name !== 'dGold' && name !== 'dSilver' && name !== 'dCopper') {
            this.setState({ isSaving: true })
            this.debounce_update_campaign()
        }
    }

    toggleNotes() {
        const { showNotes } = this.state
        this.setState({ showNotes: !showNotes })
    }

    componentDidMount() {
        this.loadCampaignOrRedirect()

    }

    async createCampaign() {
        const data = await create_campaign()

        if (data.data && data.data.id) {
            this.props.history.push(`/rpgmanager/` + data.data.id)
            this.setState({ campaign: data.data, roomCode: data.data.id })
        } else {
            console.log('error: could not create new campaign')
        }
    }

    async loadCampaignOrRedirect() {
        const { roomCode } = this.state
        if (!!roomCode) {
            const data = await get_campaign(roomCode)
            if (data.status === 200) {
                const { campaign: oldCampaign } = this.state
                const updatedCampaign = { ...oldCampaign, ...data.data }
                this.setState({ campaign: updatedCampaign, loadFailed: false })
            } else {
                this.setState({ loadFailed: true })
            }
        }
    }

    /*
    Posts current values for campaign to backend
    */
    async update_campign() {
        const { roomCode, campaign } = this.state
        
        await update_campaign(roomCode, campaign)

        this.setState({ isSaving: false})
    }

    /*
    Posts values to backend but forces an update
    */
    async update_campaign_force() {
        const { roomCode, campaign } = this.state
        
        const data = await update_campaign(roomCode, campaign)

        if (data.status === 200) {
            const updatedCampaign = { ...campaign, ...data.data }
            this.setState({ campaign: updatedCampaign })
        }

        this.setState({ isSaving: false})
    }

    debounce_update_campaign = debounce(750, this.update_campign)

    async createCharacter() {
        const { roomCode, campaign: oldCampaign } = this.state
        const data = await create_character(roomCode)
        if (data.status === 200) {
            const updatedCampaign = { ...oldCampaign, ...data.data }
            this.setState({ campaign: updatedCampaign })
        }
    }

    deleteCharacter = (id) => async () => {
        const { roomCode, campaign: oldCampaign } = this.state
        const data = await delete_character(roomCode, id)
        if (data.status === 200) {
            const updatedCampaign = { ...oldCampaign, ...data.data }
            this.setState({ campaign: updatedCampaign })
        }
    }

    calcMoney = (id) => async (isAddition) => {
        const { roomCode, campaign: oldCampaign } = this.state

        // pull out character
        var character = {}

        // iterate through characters and set delta values to empty string
        const characters = oldCampaign.characters.map((c) => {
            if (c.id === id) {
                character = c
                return { ...c, dGold: null, dSilver: null, dCopper: null }
            } else {
                return c
            }
        })

        // reset delta values to null
        this.setState({ campaign: { ...oldCampaign, characters }, isSaving: true })

        // make api call to calc money
        const data = { ...character, add: isAddition }

        const response = await calc_money(roomCode, data)
        if (response.status === 200) {
            const updatedCampaign = { ...oldCampaign, ...response.data }
            this.setState({ campaign: updatedCampaign, isSaving: false })
        }
    }

    setOldDeltaCurrencyValuesForPlayer(character) {
        // delta currency is the only value not stored on the backend
        // when the player is updated, preserve dGold, dSilver,and dCopper
        // if this is not done, user can enter a delta value, update something else
        // and lose the delta value
        const { id } = character
        const oldCharacter = this.getCharById(id)
        if (!!oldCharacter) {
            const newCharacter = {
                ...character,
                dGold: oldCharacter.dGold,
                dSilver: oldCharacter.dSilver,
                dCopper: oldCharacter.dCopper,
            }
            return newCharacter
        } else {
            return character
        }
    }

    getCharById(id) {
        // finds and returns a character by id, otherwise return false
        const { campaign } = this.state

        const result = campaign.characters.find((obj) => {
            return obj.id === id
        })

        if (!!result) {
            return result
        } else {
            return false
        }
    }

    render() {
        const showParty = true
        const { roomCode, loadFailed, campaign, isSaving, showNotes } = this.state

        return (
            <div>
                {!!campaign ? (
                    <div>
                        <RPGManagerHeader
                            campaign={campaign}
                            handleChange={this.handleChange}
                            isSaving={isSaving}
                            toggleNotes={this.toggleNotes}
                        />

                        <SlideInDiv
                            show={showNotes}
                            fromDirection='right'
                            style={{ top: '2%', height: '75%', width: '85%', left: '15%' }}
                        >
                            <Notes campaign={campaign}
                                   handleChange={this.handleChange} />
                        </SlideInDiv>

                        {showParty ? (
                            <Party
                                campaign={campaign}
                                createCharacter={this.createCharacter}
                                handleCharacterChange={this.handleCharacterChange}
                                calcMoney={this.calcMoney}
                                deleteCharacter={this.deleteCharacter}
                                isSaving={isSaving}
                            />
                        ) : (
                            <Monsters />
                        )}
                    </div>
                ) : (
                    <RPGLobby
                        roomCode={roomCode}
                        loadFailed={loadFailed}
                        createGame={this.createCampaign}
                    ></RPGLobby>
                )}
            </div>
        )
    }
}

export default RPGManagerView
