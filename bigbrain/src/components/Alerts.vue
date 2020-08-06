<template>
    <v-container class="alerts">
                <v-alert
                v-for="alert in alerts" :key="alert.key"
                :type="alert.type"
                 transition="scale-transition"
                 :value="alert.value"
                 elevation="2"
                 colored-border
                 dismissible
                 border="left"
                 >
                    {{ alert.msg }}
                </v-alert>
    </v-container>
</template>
<script>
import { Bus } from '../shared/Bus.js'

function generateHexString(length) {
  var ret = "";
  while (ret.length < length) {
    ret += Math.random().toString(16).substring(2);
  }
  return ret.substring(0,length);
}

export default {
    data() {
        return {
            alerts: []
        }
    },
    created() {
        Bus.$on("alert", alert => {
            alert.key = generateHexString(5);
            alert.value = true;
            this.alerts.push(alert);
            const that = this;
            window.setTimeout(()=> {
                
                for (let i = 0; i < that.alerts.length; i++) {
                    if (alert.key == that.alerts[i].key) {
                        that.alerts[i].value = false;
                        that.alerts.splice(i, 1);
                        return;
                    }
                }

            }, 10000);
        });
    }
}
</script>
<style lang="scss" scoped>
.alerts {
    position: absolute;
    max-width: 450px;
    bottom: 20px;
    right: 20px;
    z-index: 999;
}

</style>