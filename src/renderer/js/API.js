const apiURL = 'http://saumondeluxe.ddns.net:63246/';

const connectionENDPOINT = (id, password) => `uvsq/bulletin/${id}+${password}`;
const edtENDPOINT = (classe, startdate, endate) => `uvsq/edt/${classe}+${startdate}+${endate}`;

// Partie connection
export const connection = async (id, password) => {
    try {
        const response = await fetch(apiURL + connectionENDPOINT(id, password), {
            method: 'GET',
            mode: 'cors',
            credentials: 'same-origin',
            headers: {
                'Accept': 'application/json',
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Connection error:', error);
        return { error: 'Erreur de connexion au serveur' };
    }
}

// Partie emploi du temps
export const edt = async (classe, startdate, endate) => {
    try {
        const response = await fetch(apiURL + edtENDPOINT(classe, startdate, endate), {
            method: 'GET',
            mode: 'cors',
            credentials: 'same-origin',
            headers: {
                'Accept': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('EDT error:', error);
        return { error: 'Erreur de récupération de l\'emploi du temps' };
    }
}