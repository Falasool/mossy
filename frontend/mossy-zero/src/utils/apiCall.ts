import { useAuthStore } from '@/stores/AuthStore';

interface FetchOptions {
    endpoint: string;
    data: any;
}

const baseUrl = import.meta.env.VITE_BASE_URL || ''

export async function callApi({ endpoint, data }: FetchOptions): Promise<any> {
    if (!endpoint.startsWith('/')) {
        throw new Error('Endpoint must start with /');
    }
    if (!isValidJson(data)) {
        throw new Error("Provided data is not a valid JSON object.");
    }
    const store = useAuthStore();
    const headers = new Headers({
        'Content-Type': 'application/json',
        'X-EDGE-API': 'api/v1',
    });


    if (store.token) {
        headers.append('Authorization', `Bearer ${store.token}`);
    }

    const fetchOptions: RequestInit = {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(data)
    };

    try {
        const response = await fetch(`${baseUrl}/api${endpoint}`, fetchOptions);

        if (!response.ok) {
            throw new Error(`HTTP error, status = ${response.status}`);
        }

        const responseData = await response.json();

        if (responseData.status === 'OK') {
            return responseData.payload;
        } else {
            console.error(responseData.msg);
            throw new Error(responseData.status || 'Unknown error');
        }
    } catch (error) {
        console.error('Error making api fetch call', error);
        throw error;
    }
}

function isValidJson(data: any): boolean {
    try {
        JSON.stringify(data);
        return true;
    } catch (e) {
        return false;
    }
}