<template>
  <div class="logo">
    <img src="../assets/img/cornell_logo.png">  
  </div>
  <div class="title">
    Bee Tracking System
  </div>
  <div class="sta">
    <router-link :to=" { name : 'events' } " class='btn btn_start'>Start</router-link>
  </div>
</template>

<script>
import events from '../views/Events';

export default {
  name: 'home',
  components: {
    'events' : events
  }
}
</script>

<style scoped>
.sta {
  margin-top: 120px;
}
.btn_start {
  background-color: rgb(207, 204, 204);
  border: 2px solid rgb(160, 39, 39);
  color: black;
  width: 20%;
  font-weight: 600;
  display: table-cell;
  margin:0 auto;
  display:block;
}
.btn_start:hover {
  background-color: rgb(160, 39, 39);
  color: white;
  box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
}
.title {
  font-size: 25px;
  font-weight: 900;
  color: black;
  display: flex;
  align-items: center;
  justify-content: center;
  vertical-align: center;
}
.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  vertical-align: center;
  padding-top: 120px;
}
</style>
