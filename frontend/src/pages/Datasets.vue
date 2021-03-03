<template>
  <q-page>
    <div class="q-pa-md row items-start q-gutter-md">
      <q-card v-for="(obj, index) in items" :key="index" class="col-3 text-primary">
        <q-toolbar>
          <div class="text-h6">{{obj.name}}</div>
          <q-space />
          <q-btn flat round icon="icon-settings-outline" @click="editData(obj)"/>
          <q-btn flat round icon="icon-trash-outline" @click="deleteData(obj.id)"/>
        </q-toolbar>
        <q-card-section>
           
          <div class="text-subtitle2">{{obj.engine}}://{{obj.host}}/{{obj.database}}</div>
        </q-card-section>
        <q-btn unelevated class="full-width q-pa-sm" icon="icon-log-in-outline" label="Conectar" :to="'/queries/'+obj.name"/>
      </q-card>
    </div>
    <q-dialog v-model="dialog">
      <q-card min-width = "300px">
        <q-card-section class="row items-center">
            <div class="q-pa-md">
              <div class="q-gutter-md">
                <div class="row">
                  <div class="col q-pa-xs">
                    <q-input standout="bg-primary text-white" dense v-model="item.name"  label="Nome" />
                  </div>
                  <div class="col q-pa-xs">
                    <q-select 
                    standout="bg-primary text-white"
                      v-model="item.type"
                      emit-value
                      map-options
                      dense dropdown-icon="icon-chevron-down-outline"
                      :options="$dataset_types"
                      label="Tipo" 
                    />
                  </div>
                </div>
                <div class="col-12" v-show="item.hasOwnProperty('type') && item.type=='connection'">
                    <div class="row">
                      <div class="col-6 q-pa-xs">
                        <q-select 
                          standout="bg-primary text-white"
                          v-model="item.engine"
                          emit-value
                          map-options
                          dense dropdown-icon="icon-chevron-down-outline"
                          :options="$engines"
                          label="Tipo"
                        />
                      </div>
                    </div>
                    <div class="row">  
                      <div class="col q-pa-xs">
                        <q-input standout="bg-primary text-white" dense v-model="item.database"  label="Banco de Dados" />
                      </div>  
                      <div class="col q-pa-xs">
                        <q-input standout="bg-primary text-white" dense v-model="item.host"  label="Host" />
                      </div>
                    </div>
                    <div class="row">
                      <div class="col q-pa-xs">
                        <q-input standout="bg-primary text-white" dense v-model="item.username"  label="Usuário" />
                      </div>
                      <div class="col q-pa-xs">
                        <q-input standout="bg-primary text-white" dense v-model="item.password"  label="Senha" />
                      </div>
                    </div>
                </div>
                <div  class="row" v-show="item.hasOwnProperty('type') && item.type=='file'">
                  teste2
                </div>
              </div>
            </div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Salvar" color="primary" v-close-popup @click="saveData()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <q-btn fab icon="icon-add-outline" color="primary" @click="dialog = true"/>
    </q-page-sticky>
  </q-page>
</template>

<script>
import Database from 'components/Database';
export default {
  name: 'Datasets',
  extends: Database,
  data:()=>({
    params: {},
    endpoint: '/api/auth/datasets'
  }),
  methods:{
  },
  mounted(){
    let _this = this;
    _this.listData();
  }
}
</script>
