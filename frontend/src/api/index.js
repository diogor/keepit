import axios from 'axios'

const API_URL = process.env.VUE_APP_API_URL || "http://127.0.0.1:8000"


export const fetchContactList = async (token) => {
    let contacts = []

    const response = await axios.get(`${API_URL}/`, {
        headers: {
            'Authorization': `Token ${token}`
        }
    })

    contacts = response.data

    return contacts
}

export const fetchContact = async (id, token) => {
    let contact = {}

    const response = await axios.get(`${API_URL}/${id}`, {
        headers: {
            'Authorization': `Token ${token}`
        }
    })

    contact = response.data

    return contact
}

export const deleteContact = async (id, token) => {
    await axios.delete(`${API_URL}/${id}`, {
        headers: {
            'Authorization': `Token ${token}`
        }
    })
}

export const login = async (username, password) => {
    const response = await axios.post(`${API_URL}/token`, {
        username, password
    })
    return response.data.token
}

export const showDate = (dateobj) => {
    return new Date(dateobj).toLocaleString()
}