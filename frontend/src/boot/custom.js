import Vue from 'vue';
import _ from 'lodash';
import axios from 'axios';
import VueCodemirror from 'vue-codemirror';
import 'codemirror/lib/codemirror.css';
import 'codemirror/mode/sql/sql.js';
import 'codemirror/theme/dracula.css';
import 'codemirror/addon/scroll/simplescrollbars.css';
import 'codemirror/addon/scroll/simplescrollbars.js';
Vue.use(VueCodemirror,{
    options:{
        tabSize: 4,
        mode: 'sql',
        scrollbarStyle: 'overlay',
        theme: 'dracula',
        lineNumbers: true,
        line: true,
    }
});

Vue.prototype.$axios = axios;
Vue.prototype.$scroll_style = {
  thumb: {
    right: '4px',
    borderRadius: '5px',
    backgroundColor: '#bcd',
    width: '6px',
    opacity: 1
  },
  bar: {
    opacity: 0.0
  }
};
const token = localStorage.getItem('user-token')
if (token) {
  axios.defaults.headers.common['Authorization'] = token;
}

Vue.prototype.$getRoutes= (obj)=>{
  let _this = obj
  for(let index in _this.$router.options.routes){ 
    if(_this.$router.options.routes[index].path =='/'+_this.$route.path.split('/')[1]){
     return _this.$router.options.routes[index].children
    }
  }
}

Vue.prototype.$dataset_types = [
    {label:'Conexão',value:'connection'},
    {label:'Arquivo',value:'file'}
]

Vue.prototype.$engines = [
    {label:'Oracle',value:'oracle'},
    {label:'SQL Server',value:'mssql+pymssql'},
    {label:'MySQL',value:'mysql'},
    {label:'PostgreSQL',value:'postgresql+psycopg2'},
]
