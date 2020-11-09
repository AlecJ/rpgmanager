import * as restAPI from './base'

export const fetch_good_morning_data = async (id) => {
    try {
        const response = await restAPI.get(`/goodmorning`)
        return response
    } catch (error) {
        return {}
    }
}
