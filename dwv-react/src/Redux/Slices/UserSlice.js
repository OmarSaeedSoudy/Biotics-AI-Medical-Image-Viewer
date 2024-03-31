import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  name: "",
  role: ""
}

export const UserSlice = createSlice({
  name: 'User',
  initialState,
  reducers: {
    setUser: (state, action) => {
      console.log("Set user Called")
        state.name = action.payload.name
        state.role = action.payload.role
        console.log("el action: ", action)
    },
  },
})

// Action creators are generated for each case reducer function
export const { setUser } = UserSlice.actions

export default UserSlice.reducer