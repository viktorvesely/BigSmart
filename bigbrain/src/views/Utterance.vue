<template>
    <v-container fill-height fluid>
        
                <div style="position: absolute; top: 20%; width: 100%">
                    <h1 style="text-align: center;">Nauč ma niečo</h1>
                    <v-text-field class="centered-input" v-model="utterance" @input="query"></v-text-field>     
                </div>
                <v-card v-if="utterance !== ''" class="pa-15" style="position: absolute; top: 35%; width: 95%; left: 3%; transition: height 0.1s;">
                    
                    <h2 style="text-align: center; margin-right: 5px;">Predikcia</h2>
                    <v-card-actions>
                        <div v-if="loading" class="text-center" style="width: 100%;">
                            <v-progress-circular
                            indeterminate
                            color="primary"
                            ></v-progress-circular>
                        </div>
                        <v-container v-if="!loading">
                            <v-row justify="center" class="mt-5 mb-2">
                                <v-spacer v-if="confidence === -1"></v-spacer>
                                <v-col col="2" justify="center" text-align="center">
                                    <v-combobox ref="input" no-data-text="Vytvoriť nový intent" spellcheck="false" v-model="prediction" dense :items='options' @change="selectIntent" label="Intent" class="primary--text">
                                
                                    </v-combobox>
                                </v-col>
                                <v-spacer></v-spacer>
                                <v-col v-if="confidence !== -1" col="3" class="pt-5">
                                    <span> verím tomu na <b>{{ confidence }}%</b></span>
                                </v-col>
                            </v-row>
                            <v-row justify="center">
                                <v-btn color="primary" @click="validate">
                                    <span>Potvrdiť <v-icon class="ml-2">mdi-check</v-icon></span>
                                </v-btn>
                            </v-row>
                        </v-container>
                    </v-card-actions>
                </v-card>
    </v-container>
</template>
<script>
import axios from "axios"

import { Bus } from "../shared/Bus.js"

const URL = "http://127.0.0.1:5000"

export default {
    data: () => ({
        utterance: "",
        timer: null,
        prediction: "",
        confidence: -1,
        options: [],
        loading: false
    }),
    created() {
        this.loadIntents();
    },
    methods: {
        loadIntents() {
            axios.get(this.url("/intents")).then(response => {
            let intents = response.data.intents;
            this.options = intents;
        });
        },
        query(e) {
            this.loading = true;
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
                    this.loading = false;
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
            let found = false;
            for(let i = 0; i < this.options.length; i++) {
                let option = this.options[i];
                if (option === intent) {
                    found = true;
                    break;
                }
            }
            this.found = found;
            if (!found) {
                this.options.push(intent);
            }
        },
        validate() {
            let request = {
                utterance: this.utterance,
                intent: this.prediction
            }
            axios.post(this.url("/utterance"), request).then(response => {
                let data = response.data;
                if (data.error) {
                    Bus.$emit("alert", {
                        type: "error",
                        msg: data.error
                    });
                    return;
                }
                let offset = data.train_time; // in seconds
                let trainingTime = new Date();
                trainingTime.setSeconds(trainingTime.getSeconds() + offset);
                let hours = trainingTime.getHours();
                let seconds = trainingTime.getSeconds();
                let minutes = trainingTime.getMinutes();
                if (!this.found) {
                     Bus.$emit("alert", {
                        type: "success",
                        msg: "Nový intent bol vytvorený!"
                    });
                }
                Bus.$emit("alert", {
                    type: "info",
                    msg: `Tréning bol naplánový na ${hours}:${minutes}:${seconds}`
                });
            }).catch(error => {
                Bus.$emit("alert", {
                    type: error,
                    msg: "Bohužuaľ došlo k chybe pri validácií"
                })
            });
        }
    }
}
</script>
<style lang="scss">
.centered-input input {
  text-align: center
}
</style>