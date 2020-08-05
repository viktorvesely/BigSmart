<template>
    <v-container fill-height fluid>
        <v-row >
            <v-col style="padding: 0 55px;">
                <h2 style="text-align: center;">Nauč ma niečo</h2>
                <v-text-field class="centered-input" v-model="utterance" @input="query">
                    
                </v-text-field>
                <v-card v-if="prediction !== ''" class="pa-15">
                    <v-card-actions>
                        <v-container>
                            <v-row justify="center">
                                <v-col col="3">
                                    <v-autocomplete no-data-text="Nič som nenašiel" spellcheck="false" v-model="prediction" dense :items='options' @change="selectIntent" label="Predikcia" class="primary--text">
                                
                                    </v-autocomplete>
                                </v-col>
                                <v-spacer></v-spacer>
                                <v-col col="3" class="pt-5">
                                    <span v-if="confidence !== -1"> verím tomu na <b>{{ confidence }}%</b></span>
                                </v-col>
                            </v-row>
                        </v-container>
                    </v-card-actions>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
import axios from "axios"

const URL = "http://127.0.0.1:5000"

export default {
    data: () => ({
        utterance: "",
        timer: null,
        prediction: "",
        confidence: -1,
        options: []
    }),
    created() {
        axios.get(this.url("/intents")).then(response => {
            let intents = response.data.intents;
            this.options = intents;
        });
    },
    methods: {
        query(e) {
            if (this.timer) {
                window.clearTimeout(this.timer);
                this.timer = null;
            }
            const that = this;
            this.timer = window.setTimeout(() => {
                that.predict.call(that);
            }, 800);
        },
        url(path) {
            return URL + path;
        },
        predict() {
            if (this.utterance) {
                axios.post(this.url("/predict"), {utterance: this.utterance, user: false}).then(response => {
                    let data = response.data;
                    this.prediction = data.intent;
                    this.confidence = Math.round(100 * data.confidence);
                });
            } else {
                this.prediction = "";
                this.confidence = -1;
            }
        },
        selectIntent(intent) {
            this.confidence = -1;
        }
    }
}
</script>
<style lang="scss">
.centered-input input {
  text-align: center
}
</style>