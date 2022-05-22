<template>
  <span class="avatar-dropdown">
    <!--<el-avatar class="user-avatar" :src="avatar"></el-avatar>-->
    <img class="user-avatar" :src="avatar" alt="" />
    <div class="user-name">
      {{ username }}
    </div>
  </span>
</template>

<script>
  import { mapGetters } from 'vuex'

  export default {
    name: 'VabAvatar',
    computed: {
      ...mapGetters({
        avatar: 'user/avatar',
        username: 'user/username',
      }),
    },
    methods: {
      handleCommand(command) {
        switch (command) {
          case 'github':
            window.open('https://github.com/Columbine21')
            break
        }
      },
    },
  }
</script>
<style lang="scss" scoped>
  .avatar-dropdown {
    display: flex;
    align-content: center;
    align-items: center;
    justify-content: center;
    justify-items: center;
    height: 50px;
    padding: 0;

    .user-avatar {
      width: 40px;
      height: 40px;
      cursor: pointer;
      border-radius: 50%;
    }

    .user-name {
      position: relative;
      margin-left: 5px;
      margin-left: 5px;
      cursor: pointer;
    }
  }
</style>
