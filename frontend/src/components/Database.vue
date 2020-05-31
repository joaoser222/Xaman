<template>
</template>
<script>
export default {
  name: 'Database',
  data: ()=>({
    dialog: false,
    endpoint: '',
    item: {},
    items: {},
  }),
  methods:{
    saveData(){
      let _this = this;
      _this.$axios.post(_this.endpoint,_this.item)
      .then((response)=>{
        _this.listData();
      }).catch((err)=>{
        _this.$dialog('Erro',err.message,{},_this.listData());
      }).finally(()=>{
        _this.item = Object.assign({});
      });
    },
    editData(item){
      let _this = this;
      _this.item = Object.assign({},item);
      _this.dialog = true;
    },
    deleteData(id){
      let _this = this;
      _this.$q.dialog({
          title: 'Excluir?',
          message: 'Deseja realmente excluir o item selecionado?',
          persistent: false,
          class: 'bg-secondary text-warning',
          ok:{label: 'Sim'},
          cancel:{label: 'Não'}
        }).onOk(()=>{
            _this.$axios({url: _this.endpoint,data: {'id': id}, method: 'DELETE'})
            .then((result)=>{
              _this.listData();
            })
            .catch((err)=>{
            _this.$q.dialog({
                title: 'Excluir?',
                message: err,
                persistent: false,
                class: 'bg-secondary text-negative',
                ok:{label: 'Ok'}
              });
            });
        });
    },
    listData(){
      let _this = this;
      _this.$axios.get(_this.endpoint)
      .then((response)=>{
          _this.items = response.data;
      });
    }
  }
}
</script>