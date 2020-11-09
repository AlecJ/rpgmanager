import * as restAPI from './base'

export const get_campaign = async (id) => {
    try {
        const response = await restAPI.get(`/rpgmanager/campaign`, { campaignId: id })
        return response
    } catch (error) {
        return {}
    }
}

export const create_campaign = async () => {
    try {
        const response = await restAPI.post(`/rpgmanager/campaign`)
        return response
    } catch (error) {
        return {}
    }
}

export const update_campaign = async (id, data) => {
    try {
        const response = await restAPI.put(`/rpgmanager/campaign`, { campaignId: id, data: data })
        return response
    } catch (error) {
        return {}
    }
}

export const create_character = async (id) => {
    try {
        const response = await restAPI.post(`/rpgmanager/character`, { campaignId: id })
        return response
    } catch (error) {
        return {}
    }
}

export const update_character = async (id, character) => {
    try {
        const response = await restAPI.post(`/rpgmanager/character`, {
            characterId: id,
            character: character,
        })
        return response
    } catch (error) {
        return {}
    }
}

export const delete_character = async (campaignId, characterId) => {
    try {
        const response = await restAPI.deleto(`/rpgmanager/character`, {
            campaignId,
            characterId,
        })
        return response
    } catch (error) {
        return {}
    }
}

export const calc_money = async (campaignId, data) => {
    try {
        const response = await restAPI.put(`/rpgmanager/character`, {
            campaignId,
            data,
        })
        return response
    } catch (error) {
        return {}
    }
}
