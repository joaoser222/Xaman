<template>
  <q-layout view="lHh Lpr lFf">
    <q-header>
      <q-btn-group spread>
        <q-btn
          v-for="route in routes" 
          :key="route.path" 
          type="a"
          :icon="route.icon"
          :href="base_url+'/#/'+root_path+'/'+route.path" 
          :label="route.name"
          class="q-pa-sm"
          push
          flat
        />
      </q-btn-group>
    </q-header>
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
export default {
  name: 'MainLayout',
  data () {
    return {
      root_path: this.$route.path.split('/')[1],
      base_url: window.location.origin,
      leftDrawerOpen: false,
      routes: {}
    }
  },
  mounted(){
    let _this = this;
    _this.routes = _this.$getRoutes(_this);
  }
}
</script>