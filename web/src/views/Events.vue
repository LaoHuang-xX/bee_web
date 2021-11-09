<template>
  <navi></navi>
  <div class="container">
      <div class="con img_win">
        <transition-group name="fade" tag="div">
          <div class="slider" v-for="i in [currentIndex]" :key="i">
            <img  class="im" :src="currentImg1" />
            <img  class="im" :src="currentImg2" />
            <img  class="im" :src="currentImg3" />
            <img  class="im" :src="currentImg4" />
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
      //imgs: ["2021-08-28_18-36-23_427832_side-3_1.jpg", "2021-08-28_18-36-23_499866_side-3_2","2021-08-28_18-36-23_568734_side-3_3","2021-08-28_18-36-23_634909_side-3_4","2021-08-28_18-36-23_706691_side-3_5","2021-08-28_18-36-23_751908_side-3_6","2021-08-28_18-36-23_799163_side-3_7","2021-08-28_18-36-23_863653_side-3_8",],
      imgs: ["1.jpg", "2.jpg","3.jpg","4.jpg","5.jpg","6.jpg","7.jpg","8.jpg", "9.jpg","10.jpg","11.jpg","12.jpg"], 
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
      this.currentIndex += 4;
    },
    prev : function() {
      this.currentIndex -= 4;
    },
    incr : function() {
      this.currentIndex += 4;
    }
  },
  computed: {
    currentImg1: function() {
      return require('../assets/img/' + this.imgs[Math.abs(this.currentIndex) % this.imgs.length]) ; //first image
    },
    currentImg2: function() {
      return require('../assets/img/' + this.imgs[Math.abs(this.currentIndex) % this.imgs.length + 1]) ; //second image
    },
    currentImg3: function() {
      return require('../assets/img/' + this.imgs[Math.abs(this.currentIndex) % this.imgs.length + 2]) ; //thire image
    },
    currentImg4: function() {
      return require('../assets/img/' + this.imgs[Math.abs(this.currentIndex) % this.imgs.length + 3]) ; //forth image
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
