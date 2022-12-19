import axios from 'axios'
import { server, analysis } from 'context'

 export const apiStroke = req => axios.post(`${server}${analysis}stroke`, req)