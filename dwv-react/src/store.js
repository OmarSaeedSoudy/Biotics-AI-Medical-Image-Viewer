import { configureStore } from '@reduxjs/toolkit'
import UserSlice from './Redux/Slices/UserSlice'

export const store = configureStore({
  reducer: {
    User: UserSlice
  },
})