import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  patientsList: [],
}

export const PatientsSlice = createSlice({
  name: 'Patients',
  initialState,
  reducers: {
    setPatients: (state, action) => {
        state.patientsList = action.payload.patientsList
    },
  },
})

// Action creators are generated for each case reducer function
export const { setPatients } = PatientsSlice.actions

export default PatientsSlice.reducer