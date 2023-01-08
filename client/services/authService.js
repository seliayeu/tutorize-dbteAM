import axios from 'axios'
const baseUrl = 'http://localhost:5000'

const signIn = async (credentials, callback) => {
  const response = await axios.post(`${baseUrl}/login`, credentials);
  if (response.status === 200) {
    console.log('poggers');
    callback(credentials, response.data);
  }
  return response.data;
};

const signUp = async (credentials, callback) => {
  const response = await axios.post(`${baseUrl}/register`, credentials);
  if (response.status === 200) {
    console.log('poggers');
    callback(credentials, response.data);
  }
  return response.data;
};

const authServices = { signIn, signUp }

export default authServices