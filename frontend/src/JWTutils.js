const access_token_name = 'access_token'

export function decodeJWT(token) {
  try {
    const base64Url = token.split('.')[1]
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(c => {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
    }).join(''))
    return JSON.parse(jsonPayload)
  } catch (e) {
    console.error('Error decoding JWT:', e)
    return null
  }
}

export const getUserIdFromToken = () => {
  const token = getAccessToken()
  if (token) {
    const decoded = decodeJWT(token)
    return decoded?.user_id
  }
  return null
}

export const getUserGroupsFromToken = () => {
  const token = getAccessToken()
  if (token) {
    const decoded = decodeJWT(token)
    return decoded?.groups
  }
  return null
}

export function isTokenValid(token) {
  if (!token) return false
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.exp * 1000 > Date.now()
  } catch {
    return false
  }
}

export const getAccessToken = () => {
  return localStorage.getItem(access_token_name); 
}