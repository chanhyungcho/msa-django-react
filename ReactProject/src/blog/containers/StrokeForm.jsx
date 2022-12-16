import Stroke from "../components/Stroke"


const StrokeForm = () => {
    const onClick = ()=> {
        
        Stroke()
    }
    return(
    
    <button onClick={onClick}> 가보장 </button>
    
    )
}

export default StrokeForm