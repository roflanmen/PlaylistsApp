(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d0d6d35"],{"73cf":function(e,t,s){"use strict";s.r(t);var r=function(){var e=this,t=e._self._c;return t("main",[t("h1",{staticClass:"page-title"},[e._v("Register")]),t("div",{staticClass:"wrapper"},[t("form",{staticClass:"register-form",on:{submit:function(t){return t.stopPropagation(),t.preventDefault(),e.submit.apply(null,arguments)}}},[t("label",{attrs:{for:"username"}},[e._v("Username:")]),t("input",{directives:[{name:"model",rawName:"v-model",value:e.username,expression:"username"}],staticClass:"form-input",attrs:{type:"text"},domProps:{value:e.username},on:{input:function(t){t.target.composing||(e.username=t.target.value)}}}),t("br"),t("label",{attrs:{for:"password"}},[e._v("Password:")]),t("input",{directives:[{name:"model",rawName:"v-model",value:e.password,expression:"password"}],staticClass:"form-input",attrs:{type:"password"},domProps:{value:e.password},on:{input:function(t){t.target.composing||(e.password=t.target.value)}}}),t("br"),t("label",{attrs:{for:"confirm-password"}},[e._v("Confirm Password:")]),t("input",{directives:[{name:"model",rawName:"v-model",value:e.confirmPassword,expression:"confirmPassword"}],staticClass:"form-input",attrs:{type:"password"},domProps:{value:e.confirmPassword},on:{input:function(t){t.target.composing||(e.confirmPassword=t.target.value)}}}),t("br"),t("label",{attrs:{for:"role"}},[e._v("Role:")]),t("select",{directives:[{name:"model",rawName:"v-model",value:e.role,expression:"role"}],staticClass:"form-input",attrs:{id:"role"},on:{change:function(t){var s=Array.prototype.filter.call(t.target.options,(function(e){return e.selected})).map((function(e){var t="_value"in e?e._value:e.value;return t}));e.role=t.target.multiple?s:s[0]}}},[t("option",{attrs:{value:"",disabled:""}},[e._v("Select role...")]),t("option",{attrs:{value:"regular"}},[e._v("Regular")]),t("option",{attrs:{value:"admin"}},[e._v("Admin")])]),t("br"),t("button",{staticClass:"form-button",on:{click:function(t){return t.stopPropagation(),t.preventDefault(),e.submit()}}},[e._v("Register")])])])])},a=[],o=(s("14d9"),{data(){return{username:"",password:"",confirmPassword:"",role:""}},computed:{isAdmin(){return"admin"===this.role}},methods:{submit(){this.username&&this.password&&this.password===this.confirmPassword&&this.role&&fetch("/api/user/",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({username:this.username,password:this.password,is_admin:this.isAdmin})}).then(e=>e.json()).then(e=>{e.message?alert(e.message):this.$router.push({name:"Login"})})}}}),n=o,i=s("2877"),l=Object(i["a"])(n,r,a,!1,null,null,null);t["default"]=l.exports}}]);
//# sourceMappingURL=chunk-2d0d6d35.2c0272a8.js.map