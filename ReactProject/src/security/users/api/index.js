import axios from 'axios'
import { server, users } from '../../../context'


export const blogLogin = req => axios.post(`${server}${users}login`, req)