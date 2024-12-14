const apiURL = 'http://localhost:8000/';

const connectionENDPOINT = (id, password) => `uvsq/bulletin/${id}+${password}`;
const edtENDPOINT = (classe, startdate, endate) => `/uvsq/edt/${classe}+${startdate}+${endate}`;

// Partie connection
export const connection = async (id, password) => {
    try {
        const response = await fetch(apiURL + connectionENDPOINT(id, password), {
            mode: 'cors'
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(error);
    }
}

// Partie emploi du temps
export const edt = async (classe, startdate, endate) => {
    try {
        const response = await fetch(apiURL + edtENDPOINT(classe, startdate, endate), {
            mode: 'cors'
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(error);
    }
}