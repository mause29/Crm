import { configureStore, createSlice } from '@reduxjs/toolkit';

const userSlice = createSlice({
    name: 'user',
    initialState: { token: null, role: null, name: null, theme: 'light' },
    reducers: {
        setUser: (state, action) => { return { ...state, ...action.payload }; },
        setTheme: (state, action) => { state.theme = action.payload; }
    }
});

export const { setUser, setTheme } = userSlice.actions;

export const store = configureStore({ reducer: { user: userSlice.reducer } });
