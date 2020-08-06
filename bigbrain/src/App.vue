<template>
  <v-app>
    <Alerts></Alerts>
    <v-main>
      <v-navigation-drawer app permanent expand-on-hover class="primary inline-block">
      <v-list nav>
        <v-list-item
          v-for="item in items"
          :key="item.title"
          link
          class="mb-4"
          :to="item.to"
        >
          <v-list-item-icon>
            <v-icon color="secondary">{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title class="secondary--text">{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>

import Alerts from "./components/Alerts.vue"

export default {
  name: 'App',
  data: () => ({
    items: [
      {
        title: "Učiť",
        icon: "mdi-alphabetical-variant",
        to: "/"
      },
      {
        title: "Intents",
        icon: "mdi-book",
        to: "/intents"
      },
      {
        title: "Užívatelia mi píšu",
        icon: "mdi-message",
        to: "/texts"
      },
      {
        title: "Budovač odpovedí",
        icon: "mdi-graph",
        to: "/builder"
      }
    ]
  }),
  components: {
    "Alerts": Alerts
  }
};
</script>
