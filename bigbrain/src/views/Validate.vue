<template>
    <v-container fill-height fluid class="pa-0">
        <v-row justify="center">
            Bohužuaľ nič tu nie je
        </v-row>
    </v-container>
</template>
<script>
import axios from "axios"

const URL = "http://127.0.0.1:5000"

export default {
    data: () => ({
        current: "",
        options: []
    }),
    created() {
        this.loadIntents();
    },
    methods: {
        selectIntent(intent) {
            console.log(intent);
        },
        url(path) {
            return URL + path;
        },
        loadIntents() {
            axios.get(this.url("/intents")).then(response => {
                let intents = response.data.intents;
                this.options = intents;
            });
        }
    }
}
</script>
