<template>
  <navi></navi>
  <div class="container">
      <div class="con img_win">
        <transition-group name="fade" tag="div">
          <div class="slider" v-for="i in [currentIndex]" :key="i">
            <img  class="im" :src="currentImg" />
            <img  class="im" :src="currentImg" />
            <img  class="im" :src="currentImg" />
            <img  class="im" :src="currentImg" />
          </div>
        </transition-group>
        <a class="prev" @click="prev" href="#">&#10094; Previous</a>
        <a class="next" @click="next" href="#">&#10095; Next</a>
      </div>
      <div class="con text_win"></div>
  </div>
</template>

<script>
import navi from '../components/Navigation.vue';

export default {
  name: 'Events',
  data() {
    return {
      imgs: ["test_1.jpg", "test.jpg", "cornell.png"],
      timer: null,
      currentIndex: 0
    };
  },
  props: {
    msg: String
  },
  components: {
    'navi' : navi
  },
  methods: {
    next: function() {
      this.currentIndex += 1;
    },
    prev : function() {
      this.currentIndex -= 1;
    },
    incr : function() {
      this.currentIndex += 1;
    }
  },
  computed: {
    currentImg: function() {
      return require('../assets/img/' + this.imgs[Math.abs(this.currentIndex) % this.imgs.length]);
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.container {
  margin: auto;
  width: 80%;
  padding: 5%;
  display: flex;
  justify-content: center;
  vertical-align: center;
}
.con {
  margin: 5%;
}
.img_win {
  background: rgb(241, 239, 239);
  border-radius: 25px;
  height: 500px;
  width: 80%;
  float: left;
  box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
}
.text_win {
  background: rgb(241, 239, 239);
  border-radius: 25px;
  height: 400px;
  width: 50%;
  box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
}
.slider {
  margin: 0 auto;
  margin-top: 30px;
  width: 90%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 3px solid green;
}
.im {
  margin-left: 2px;
  margin-right: 2px;
  height: 20%;
  width: 20%;
}

.prev, .next {
  cursor: pointer;
  top: 40%;
  width: auto;
  padding: 16px;
  color: black;
  font-weight: bold;
  font-size: 15px;
  transition: 0.7s ease;
  border-radius: 15px;
  text-decoration: none;
  user-select: none;
}

.next {
  right: 0;
}

.prev {
  left: 0;
}

.prev:hover, .next:hover {
  border: 4px solid rgb(105, 104, 104);
}
</style>
