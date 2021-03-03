<template>
  <q-layout view="lHh Lpr lFf">
    <q-header class="q-ma-sm bg-transparent">
      <q-toolbar class="bg-accent rounded-borders">
        <q-btn
          flat
          dense
          round
          @click="drawer = !drawer"
          icon="icon-menu-outline"
          aria-label="Menu"
        />
        <q-btn flat dense no-caps icon="icon-folder-outline" @click="openFile()">&nbsp;Abrir</q-btn>
        <q-btn flat dense no-caps icon="icon-save-outline">&nbsp;Salvar</q-btn>
        <q-btn flat dense no-caps icon="icon-play-outline" @click="sendQuery()">&nbsp;Executar</q-btn>
        <q-btn flat dense no-caps icon="icon-document-text-outline">&nbsp;Exportar</q-btn>
      </q-toolbar>
    </q-header>
    <q-drawer
        v-model="drawer"
        :width="300"
        bordered
        show-if-above
    >
      <q-scroll-area
        :thumb-style="$scroll_style.thumb"
        :bar-style="$scroll_style.bar"
        style="height: 100vh;"
      >
        <recursive-list
          :nodes="server.children"
          :icon="server.icon"
          :label="server.label"
          :inset="0"
        />
      </q-scroll-area>
    </q-drawer>
    <q-page-container>
      <q-page>
        <q-tabs
          v-model="selected_tab"
          dense
          class="text-grey"
          active-color="primary"
          indicator-color="primary"
          align="left"
          narrow-indicator
        >
          <q-tab          
            v-for="(item,index) in tabs" 
            :key="index"
            :name="item.name"
            dense
            no-caps
            inline-label
            >
            <div>
              {{item.label}}
              <q-btn unelevated round class="q-ml-xs" size="xs" icon="icon-close-outline" @click="dropTab(index)" v-show="tabs.length>1"></q-btn>
            </div>
          </q-tab>
          <q-btn flat round size="sm" icon="icon-add-outline" @click="addTab()"/>
        </q-tabs>
        <q-tab-panels v-model="selected_tab" class="bg-transparent">
          <q-tab-panel v-for="(item,index) in tabs" :key="index" :name="item.name">
            <q-splitter
                v-model="item.splitter"
                :limits="[30, 100]"
                horizontal
                style="height: 100%"
              >
                <template v-slot:before>
                  <div class="q-ma-sm shadow-8">                
                   <codemirror v-model="item.code"></codemirror>
                  </div>
                </template>
                <template v-slot:after>
                  <q-table 
                    separator="cell" 
                    class="q-mx-sm q-my-md shadow-8"
                    :data="item.table.data"
                    :columns="item.table.headers"
                    :loading="item.table.loading"
                    
                    bordered
                    virtual-scroll
                    :virtual-scroll-item-size="48"
                    :virtual-scroll-sticky-size-start="48"
                    :pagination="item.pagination"
                    :rows-per-page-options="[0]"
                    v-if="item.table.data.length"
                  />
                </template>

            </q-splitter>
            
          </q-tab-panel>
        </q-tab-panels>
      </q-page>
    </q-page-container>
  </q-layout>
</template>
<script>
import FileManager from 'components/FileManager.vue';
import RecursiveList from 'components/RecursiveList.vue';
export default {
    components: {
      RecursiveList
    },
    data: ()=>({
        drawer: true,
        selected_tab: null,
        tabs_number: 0,
        tabs: [],
        dataset: [],
        server: {},
        thumbStyle: {
            right: '4px',
            borderRadius: '5px',
            backgroundColor: '#ababab',
            width: '5px',
            opacity: 0.75
        },
        barStyle: {
            right: '2px',
            borderRadius: '9px',
            backgroundColor: '#000000',
            width: '9px',
            opacity: 0.2
        },
    }),
    methods:{
      getDataset(){
        let _this = this;
        _this.$axios.get('/api/auth/datasets?dataset='+_this.$route.params.server)
        .then((response)=>{
          _this.dataset = response.data.dataset;
          _this.server = {
            label: `${response.data.dataset['name']}: ${response.data.dataset['host']}/${response.data.dataset['database']}`,
            icon:'icon-server',
            children: [...JSON.parse(JSON.stringify(response.data.objects))]
          };
        });      
      },
      addTab(file_path='',file_content=''){
        let _this = this;
        _this.tabs_number += 1;

        let new_tab = {
          name:`query${_this.tabs_number}`,
          splitter: 50,
          label: file_path ? file_path.split('/').splice(-1)[0] :`Query${_this.tabs_number}.sql`,
          file:file_path,
          code:file_content,
          table:{
            pagination:{
              rowsPerPage: 0,
              rowsNumber: 0
            },
            loading: false,
            headers: [],
            data: [],  
          }
        };
        _this.tabs.push(new_tab);
        _this.selected_tab = new_tab.name;
      },
      dropTab(index){
        let _this = this;
        _this.tabs.forEach((element,key) => {
          if(key==index){
            _this.tabs.splice(index,1);
          }
        });
        _this.selected_tab = _this.tabs[_this.tabs.length - 1].name;
        console.log(_this.selected_tab);

      },
      openFile(){
        let _this = this;
        this.$q.dialog({
          title: 'Alert<em>!</em>',
          component: FileManager,
          parent: _this,
          extensions: '.sql',
          type: 'file',
          mode: 'open',
        }).onOk((data)=>{
          _this.addTab(data.path,data.content);
        });
      },
      sendQuery(){
        let _this = this;
        let tab = {}
        _this.tabs.forEach((element,index) => {
          if(element.name==_this.selected_tab){
            tab = element;
          }
        });
        console.log(tab);
        _this.$axios.post('/api/auth/query',{'code':tab.code,'dataset':_this.dataset})
        .then((response)=>{
          if(response.data.hasOwnProperty('error')){
            console.log(response.data.error)
          }else{
            tab.table.data = response.data.data;
            tab.table.headers = [];
            tab.rowsNumber = response.data.data.length;
            let fields = response.data.columns;
            for(let field in fields){
                tab.table.headers.push(
                  {
                    name: fields[field],
                    label: fields[field],
                    field: fields[field],
                    sortable: true
                  }
                );
              }
          }
        });
      }
    },
    mounted(){
      this.getDataset();
      this.addTab();
    }
    
}
</script>