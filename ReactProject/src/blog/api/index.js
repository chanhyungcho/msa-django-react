 import axios from 'axios'
import { analysis, server } from '../../context'

 export const userstroke = req => axios.post(`${server}${analysis}stroke`, req)