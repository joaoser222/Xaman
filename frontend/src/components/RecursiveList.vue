<template>
    <q-expansion-item
      :header-inset-level="inset"
      :expand-icon="nodes!=null ?'icon-chevron-down-outline':' '"
      :expanded-icon="nodes!=null ?'icon-chevron-up-outline':' '"
      dense
    >
      <template v-slot:header>
        <q-item-section avatar >
          <q-avatar :icon="icon"/>
        </q-item-section>
        <q-item-section>
          {{label}}
        </q-item-section>
      </template>
      <recursive-list
        v-for="(node,index) in nodes" 
        :nodes="node.children"
        :icon="node.icon"
        :label="node.label"
        :inset="inset+0.2"
        :key="index"
      >
    </recursive-list>
  </q-expansion-item>
</template>
<script>
  export default { 
    props: ['icon','label','nodes','inset'],
    name: 'recursive-list',
    data: ()=>({}),
  }
</script>