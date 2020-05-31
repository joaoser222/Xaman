<template>
  <q-dialog ref="dialog" @hide="onDialogHide">
    <q-card class="q-dialog-plugin">
        <q-card-section>
            <q-input class="q-py-sm" dense standout="bg-secondary text-white" v-model="current_dir" label="Caminho" v-if="mode=='open'" />
            <q-input class="q-py-sm" dense standout="bg-secondary text-white" v-model="current_dir" label="Nome" v-if="mode=='save'"/>
            <q-input class="q-py-sm" dense standout="bg-secondary text-white" :value="extensions" label="Extensão" readonly/>
            <q-scroll-area
                :thumb-style="$scroll_style.thumb"
                :bar-style="$scroll_style.bar"
                style="height: 200px;"
            >
                <q-list>
                    <q-item dense clickable v-ripple @click="getContentPath(`${current_dir.split('/').slice(0,-1).join('/')}`)">
                        <q-item-section avatar>
                            <q-icon color="primary" name="las la-arrow-left" />
                        </q-item-section>
                        <q-item-section>..</q-item-section>
                    </q-item>
                    <q-item dense v-for="(item,index) in items" :key="index" clickable v-ripple @click="getContentPath(`${current_dir}/${item.name}`,item.type)">
                        <q-item-section avatar>
                            <q-icon :color="item.type=='file' ? 'positive' : 'primary'" :name="item.type=='file' ? 'las la-file' : 'las la-folder'" />
                        </q-item-section>
                        <q-item-section>{{item.name}}</q-item-section>
                    </q-item>
                </q-list>
            </q-scroll-area>
        </q-card-section>
        <q-card-actions align="right">
            <q-btn flat label="Salvar" @click="onOKClick" v-if="mode=='save'"/>
            <q-btn flat label="Cancelar" @click="onCancelClick" />
        </q-card-actions>
    </q-card>
  </q-dialog>

</template>
<script>
export default {
    props:['extensions','type','mode'],
    data:()=>({
        current_dir: '',
        filename: null,
        items:[],
    }),
    methods:{
        getContentPath(path,type='folder'){
            let _this = this;
            _this.$axios.post('/api/auth/files',{'path':path,'extensions':_this.extensions})
            .then((response)=>{
                if(type=='folder'){
                    _this.items = response.data.items;
                    _this.current_dir = response.data.path;
                }else{
                    _this.onOKClick(response.data);
                }
            });
        },
        show(){
            this.$refs.dialog.show();
        },
        hide(){
            this.$refs.dialog.hide();
        },
        onDialogHide() {
            this.$emit('hide');
        },
        onOKClick(data){
            this.$q.loading.show()
            this.$emit('ok',data);
            this.hide();
        },
        onCancelClick(){
            this.hide();
        } 
    },
    mounted(){
        this.getContentPath();
    }
}
</script>