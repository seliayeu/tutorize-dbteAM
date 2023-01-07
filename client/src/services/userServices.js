import axios from 'axios'
const baseUrl = '/api/users'

const getUser = async (userId, username, callback) => {
  const response = await axios.get(`${baseUrl}/${userId}//`, {
    headers: {
      "Authorization": `Token ${token}`
    }
  })
  console.log(response)
  if (response.status === 200) {
    callback(response.data)
  }
  return response.data
}

const updateUser = async (userId, token, updatedUser, callback) => {
  const response = await axios.put(`${baseUrl}/${userId}/`, updatedUser,  {
    headers: {
      "Authorization": `Token ${token}`
    }
  })
  console.log(response)
  if (response.status === 204) {
    callback(response.data)
  }
  return response.status
}

const  userService = { getUser, updateUser }

export default userService;
