import {server} from 'context'
const dlearnService = {
    apiCrawler
}

function handleResponse(response){ 
    return response.text()
        .then(text =>{
            const data = text && JSON.parse(text)
            if(!response.ok){
                if(response.status === 401){
                    window.location.reload()
                }
                const error = (data && data.message) ||
                    response.statusText
                return Promise.reject(error)
            }
            return data
        })
    }
async function apiCrawler(id){
    const requestOption = {
        method: "GET",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(id)
    }

    fetch(`${server}webcrawler/crawler`, requestOption)
    .then(handleResponse)
    .then(data => {
        alert(JSON.stringify(data))
    })
    .catch((error) => {
        alert('error :::: '+error)
    })
}

export default dlearnService