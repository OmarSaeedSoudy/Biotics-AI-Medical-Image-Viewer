import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  allMedicalRecords: {},
};

export const MedicalRecordsSlice = createSlice({
  name: 'MedicalRecords',
  initialState,
  reducers: {
    setMedicalRecords: (state, action) => {
      state.allMedicalRecords[action.payload.key] = action.payload.medicalList;
    },
  },
});

// Action creators are generated for each case reducer function
export const { setMedicalRecords } = MedicalRecordsSlice.actions;

export default MedicalRecordsSlice.reducer;
