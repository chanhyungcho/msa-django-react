import dlearnService from "../api"



const NaverCrawler = () => {

    const onClick = e => {
 
        e.preventDefault()
        dlearnService.apiCrawler()
        .then(() => {
            alert('Crawler 연결 성공')
        })
    }
 
    return (<>
    <h2>네이버 영화 크롤러</h2>
    <button onClick ={onClick}>네이버 영화 크롤링2</button>
    <p>할 일을 등록하시면, 스케줄 목록에 출력됩니다.</p>
    </>)
}
export default NaverCrawler;