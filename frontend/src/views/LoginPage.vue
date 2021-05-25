<template>
  <v-list dark color="#191122" class="text-center" height="100%" width="100%" style="user-select:none;">
    <canvas id="bg-canvas"></canvas>

    <p id="title_top">информационно-аналитическая система</p>
    <p id="title_top">оперативного назначения</p>
    <p id="logo">САПФИР</p>

    <v-container class="text-center" style="max-width: 300px;">
      <v-form ref="form" v-model="valid" lazy-validation>
        <v-list-item>
          <v-list-item-content>
            <v-text-field v-model="usernameForm" :rules="[validations.nullFormRules]" label="Введите логин" outlined></v-text-field>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-text-field type="password" v-model="passwordForm" :rules="[validations.nullFormRules, validations.minLenRules]" label="Введите пароль" outlined></v-text-field>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-btn :disabled="!valid" color="success" class="mr-4" @click="loginUserInSystem">
              Войти в систему
            </v-btn>
          </v-list-item-content>
        </v-list-item>
      </v-form>
    </v-container>
  </v-list>
</template>

<script>
import '@/views/lib/tween_max.min.js'
import bg_stars from '../views/lib/bg_animate'
import { mapActions } from 'vuex'

export default {
  data: () => ({
    valid: true,
    usernameForm: '',
    passwordForm: '',
    validations: {
      nullFormRules: (v) => !!v || 'Поле не должно быть пустым',
      minLenRules: (v) => v && v.length >= 8 || 'Пароль должен быть не менее 8 символов'
    }
  }),

  methods: {
    ...mapActions(['authenticateUser']),

    loginUserInSystem () {
      if (this.$refs.form.validate()) {
        this.authenticateUser({
          userInformation: {
            username: this.usernameForm,
            password: this.passwordForm
          },
          config: {}
        })
      }
    }
  },

  mounted () {
    // отрисовка фона
    bg_stars('bg-canvas')
  }
}

</script>

<style scoped>

/************************************************
 * ЗАГОЛОВОК
 ************************************************/
#title_top {
    font-family: Verdana;
    font-size: 2.5em;
    font-weight: bold;
    color: #5ad01f;
}
#title_top:first-of-type {
    margin: 1.5em 0 0 0;
}

/************************************************
 * ЛОГОТИП
 ************************************************/
#logo {
  padding: 0 0 0.1em;
  margin: 0 auto;

  font-family: Verdana;
  font-size: 8em;
  font-weight: bold;
  letter-spacing: 0.05em;

  background: url("~@/assets/img/logo/logo-animation-background.gif") repeat-x;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;

  -moz-text-shadow:0 0 10px #3a6eff;
  -webkit-text-shadow:0 0 10px #3a6eff;
  text-shadow:0 0 10px #3a6eff;
}

/************************************************
 * ФОН
 ************************************************/
#bg-canvas {
 position: absolute;
    top: 0;
    left: 0;
}
</style>
