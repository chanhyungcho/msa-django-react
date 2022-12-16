// import axios from "axios";
// import {server, dlearn, vision} from 'context'
// export const iris = req => axios.post(`${server}${dlearn}iris`, req)
// export const getFashion = id => axios.get(`${server}${dlearn}fashion?id=${id}`)
// export const postFashion = id => axios.post(`${server}${dlearn}fashion?id=${id}`)

import axios from "axios";
import {server, dlearn, vision} from 'context'
const dlearnService = {
    iris, getFashion, postFashion 
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
async function iris(id){
    const requestOption = {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(id)
    }
    fetch(`${server}${dlearn}iris`, requestOption)
    .then(handleResponse)
    .then(data => {
        alert(JSON.stringify(data))
    })
    .catch((error) => {
        alert('error :::: '+error);
    });
}
async function postFashion(id){
    const requestOption = {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(id)
    }
    fetch(`${server}${dlearn}fashion`, requestOption)
    .then(handleResponse)
    .then(data => {
        alert('결과: '+JSON.stringify(data))
    })
    .catch((error) => {
        alert('error :::: '+error);
    });
}
async function getFashion(id){
    fetch(`${server}${dlearn}fashion?id=${id}`)
    .then(handleResponse)
    .then(data => {
        alert('결과: '+JSON.stringify(data))
    })
} 

export default dlearnService