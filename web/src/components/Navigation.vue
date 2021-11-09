<template>
    <div class="header">
        <div class="branding">
            <div class="logo_back">
                <router-link :to="{ name : 'events' }"><img class="small_logo" src="../assets/img/cornell.png"></router-link>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    
    components:{

    },
};
</script>
<style scoped>
* {
  box-sizing: border-box;
}
.header {
    width: 100%;
    height: 9%;
    position: fixed;
}
.branding {
    background-color: rgb(160, 39, 39);
    position: relative;
    height: 100%;
    box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
}
.logo_back {
    background-color: white;
    width: 5%;
    height: 100%;
}
.small_logo {
    position: absolute;
    width: 5%;
    height: 100%;
}
</style>