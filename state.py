class State:

    @classmethod
    def state_add(cls, st, key, value):
        if key not in st.session_state:
            st.session_state[key] = value
            return value
        return st.session_state[key]

    @classmethod
    def state_update(cls, st, key, value):
        st.session_state[key] = value

    @classmethod
    def state_remove(cls, st, key):
        del st.session_state[key]

    @classmethod
    def state_remove_multiple(cls, st, keys):
        for key in keys:
            if key in st.session_state:
                del st.session_state[key]

    @classmethod
    def state_clear(cls, st):
        st.session_state.clear()

    @classmethod
    def get_state(cls, st):
        return st.session_state

    @classmethod
    def get(cls, st, key):
        if key in st.session_state:
            return st.session_state[key]
        else:
            return None
