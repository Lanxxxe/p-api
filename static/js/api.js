const baseURL = "http://127.0.0.1:8000/api/"

/**
 * Fetch data from API endpoint (GET request)
 * @param {string} endpoint - API endpoint path
 * @returns {Promise<any>} - Response data
 */
const getData = async (endpoint) => {
    try {
        const response = await fetch(baseURL + endpoint);

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || errorData.message || `HTTP Error ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        return data;
        
    } catch (error) {
        console.error(`Error fetching data from ${endpoint}:`, error.message);
        throw error;
    }
}

/**
 * Send data to API endpoint (POST or PUT request)
 * @param {string} endpoint - API endpoint path
 * @param {string} csrfToken - CSRF token for security
 * @param {object} data - Data to send
 * @param {string} method - HTTP method ('POST' or 'PUT'), defaults to 'POST'
 * @returns {Promise<any>} - Response data
 */
const sendData = async (endpoint, csrfToken, data, method = 'POST') => {
    try {
        const response = await fetch(baseURL + endpoint, {
            method: method.toUpperCase(),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || errorData.message || `HTTP Error ${response.status}: ${response.statusText}`);
        }
        
        const responseData = await response.json();
        console.log(`${method} request successful:`, responseData);
        return responseData;
        
    } catch (error) {
        console.error(`Error sending data to ${endpoint} with ${method}:`, error.message);
        throw error;
    }
}

/**
 * Delete data from API endpoint (DELETE request)
 * @param {string} endpoint - API endpoint path
 * @param {string} csrfToken - CSRF token for security
 * @returns {Promise<any>} - Response data
 */
const deleteData = async (endpoint, csrfToken) => {
    try {
        const response = await fetch(baseURL + endpoint, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || errorData.message || `HTTP Error ${response.status}: ${response.statusText}`);
        }
        
        // DELETE requests may return 204 No Content
        if (response.status === 204) {
            return { success: true };
        }
        
        const responseData = await response.json();
        console.log('DELETE request successful:', responseData);
        return responseData;
        
    } catch (error) {
        console.error(`Error deleting data from ${endpoint}:`, error.message);
        throw error;
    }
}

/**
 * Update data at API endpoint (PUT request)
 * @param {string} endpoint - API endpoint path
 * @param {string} csrfToken - CSRF token for security
 * @param {object} data - Data to update
 * @returns {Promise<any>} - Response data
 */
const updateData = async (endpoint, csrfToken, data) => {
    return await sendData(endpoint, csrfToken, data, 'PUT');
}