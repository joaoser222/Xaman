<template>
  <q-page>
    <div class="q-pa-md row fullscreen items-center justify-center q-gutter-md">
      <q-card class="bg-secondary col-md-4 col-sm-6 ">
        <q-toolbar>
          <q-toolbar-title>
            Entrar
          </q-toolbar-title>
        </q-toolbar>
        <q-card-section class="text-white">
          <div class="row">  
            <div class="col-12 q-pa-xs" v-if="register">
              <q-input standout="bg-primary text-white" dense v-model="login.name"  label="Nome"/>
            </div> 
            <div class="col-12 q-pa-xs">
              <q-input standout="bg-primary text-white" dense v-model="login.email"  label="Email" />
            </div>   
            <div class="col-12 q-pa-xs">
              <q-input standout="bg-primary text-white" type="password" dense v-model="login.password"  label="Senha" />
            </div>
            <div class="col-12 q-pa-xs" v-if="register">
              <q-input standout="bg-primary text-white" type="password" dense v-model="login.confirm_password"  label="Confimação de Senha"/>
            </div>  
          </div>
          <div class="row text-right">  
            <div class="col q-pa-xs" v-if="register">
              <q-btn size="sm" flat @click="register = false" no-caps>Já possuo cadastro</q-btn>
            </div>
            <div class="col q-pa-xs" v-else>
              <q-btn size="sm" flat @click="register = true" no-caps>Não possuo cadastro</q-btn>
            </div>              
          </div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat @click="sendData()" :label="register ? 'Cadastrar': 'Entrar'"></q-btn>
        </q-card-actions>
      </q-card>
    </div>
  </q-page>
</template>

<script>
export default {
  name: 'Login',
  data: ()=>({
    register: false,
    login:{
      email: null,
      password: null
    }
  }),
  methods:{
    sendData(){
      let _this = this;
      let endpoint = _this.register ? '/api/register' : '/api/login';
      _this.$axios.post(endpoint,_this.login)
      .then((response)=>{
        if(response.data.hasOwnProperty('error')){
          _this.$q.dialog(
            {
              title: 'Erro!',
              message: response.data.error,
              persistent: false,
              class: 'bg-secondary text-negative',
              ok:{label: 'Ok',color:'secondary'},
            }
          );
        }else{
          _this.$store.dispatch('AuthRequest');
          _this.$q.dialog(
            {
              title: 'Sucesso!',
              message: response.data.success,
              persistent: false,
              class: 'bg-secondary text-positive',
              ok:{label: 'Ok',color:'secondary'},
            }
          ).onDismiss(function(){
            window.location.href = '/';
          });
        }
      });
    }
  }
}
</script>
