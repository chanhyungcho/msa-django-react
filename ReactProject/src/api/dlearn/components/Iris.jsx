
import { useState } from "react";
import dlearnService from "../api";


const Iris = () => {

  
    const [inputs, setInputs] = useState({})
    const {SepalLengthCm, SepalWidthCm, PetalLengthCm, PetalWidthCm} = inputs;
    
    const onChange = e => {
        e.preventDefault()
        const {value, name} = e.target
        setInputs({...inputs, [name]: value})
    }
    
    const onClick = e => {
        e.preventDefault()
        const request = {SepalLengthCm, SepalWidthCm, PetalLengthCm, PetalWidthCm}
        alert(`iris: ${JSON.stringify(request)}`)
        dlearnService.iris(request)
        .then((res)=>{
            console.log(`Response is ${res.data.result}`)
            localStorage.setItem('token', JSON.stringify(res.data.result))
            alert(`찾는 품종 : ${JSON.stringify(res.data.result)}`)
        })
        .catch((err)=>{
            console.log(err)
            alert('꽃잎,받침 길이/너비를 다시 입력해주세요')
        }) 
    }
    
    return(
    <>
    
    SepalLengthCm: <input type ="text" name="SepalLengthCm" onChange={onChange}/><br/>
    SepalWidthCm: <input type ="text" name="SepalWidthCm" onChange={onChange}/><br/>
    PetalLengthCm: <input type ="text" name="PetalLengthCm" onChange={onChange}/><br/>
    PetalWidthCm: <input type ="text" name="PetalWidthCm" onChange={onChange}/><br/>
    <button onClick={onClick}> 입력 </button>
    
    </>)}


export default Iris